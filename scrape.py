import csv
import time
import logging
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Configure logging
logging.basicConfig(filename='selenium_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Selenium Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode to avoid opening a browser window

# Set up Selenium Chrome service
webdriver_service = Service('path/to/chromedriver')

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

def scrape_laptop_data():
    try:
        # Open Daraz website
        driver.get('https://www.daraz.pk/')

        # Accept cookies if prompted
        time.sleep(2)  # Add a delay to allow time for the cookie banner to appear
        try:
            driver.find_element(By.XPATH, "//button[text()='Accept All']").click()
        except NoSuchElementException:
            pass

        # Navigate to the electronic devices category
        driver.find_element(By.XPATH, "//a[text()='Electronic Devices']").click()

        # Navigate to the laptop category
        driver.find_element(By.XPATH, "//a[text()='Laptops']").click()

        # Scrape laptop data from first 10 pages
        data = []
        for page in range(1, 11):
            # Scroll to the bottom of the page to load all laptops
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Add a delay to allow time for the page to load
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Scrape laptop data
            laptops = driver.find_elements(By.XPATH, "//div[contains(@class, 'c2prKC')]")  # Update the XPath accordingly

            for laptop in laptops:
                # Extract the required laptop details
                name = laptop.find_element(By.XPATH, ".//a[contains(@class, 'c16H9d')]").text
                price = laptop.find_element(By.XPATH, ".//div[contains(@class, 'c3gUW0')]").text
                rating = laptop.find_element(By.XPATH, ".//div[contains(@class, 'c3dn4k')]").text

                # Store the laptop details in a dictionary
                laptop_data = {
                    'Name': name,
                    'Price': price,
                    'Rating': rating
                }
                data.append(laptop_data)

                # Log the laptop details
                logging.info(f"Laptop Name: {name}, Price: {price}, Rating: {rating}")

            # Go to the next page
            next_page = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Next Page')]")
            next_page.click()

        # Save the data to a CSV file
        with open('laptop_data.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'Price', 'Rating']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

# Schedule the bot to run every 7 days
schedule.every(7).days.do(scrape_laptop_data)

while True:
    schedule.run_pending()
    time.sleep(1)
