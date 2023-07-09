import time
import logging
import warnings
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from .models import Laptop_Data, Laptop_DataSchema, db
from flask import jsonify
warnings.filterwarnings("ignore")


laptop_schema = Laptop_DataSchema()
laptop_schema = Laptop_DataSchema(many=True)

# Configure logging

# Create a logger object
logger = logging.getLogger('selenium_bot')
logger.setLevel(logging.INFO)

# Create a file handler to write info logs to the file
info_handler = logging.FileHandler('selenium_bot_info.log')
info_handler.setLevel(logging.INFO)

# Create a file handler to write error logs to the file
error_handler = logging.FileHandler('selenium_bot_error.log')
error_handler.setLevel(logging.ERROR)

# Create a formatter to specify the log message format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Set the formatter for the handlers
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(error_handler)

# Example usage
try:
    # Some code that may raise an error
    raise ValueError('An error occurred')
except Exception as e:
    logger.error(f'Error occurred: {str(e)}')


# Set up Selenium Chrome options

chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode to avoid opening a browser window
chrome_options.add_argument('--log-level=3')  # Suppress logging messages

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

def scrape_laptop_data(pages):

    print('Laptop Data Scraping Started')
    try:
        # Open Daraz website
        driver.get('https://www.daraz.pk/')

        # Accept cookies if prompted
        # Add a delay to allow time for the cookie banner to appear
        time.sleep(2)
        try:
            driver.find_element(
                By.XPATH, "//button[text()='Accept All']").click()
        except NoSuchElementException:
            pass

        # Navigate to the electronic devices category
        driver.find_element(
            By.XPATH, '//*[@id="Level_1_Category_No1"]/a/span').click()

        # Navigate to the laptop category
        driver.find_element(
            By.XPATH, '//*[@id="J_5022174600"]/div/ul/ul[7]/li[5]/a/span').click()

        # Scrape laptop data from first 10 pages
        data = []
        for page in range(1, pages + 1):
            # Scroll to the bottom of the page to load all laptops
            last_height = driver.execute_script(
                "return document.body.scrollHeight")
            while True:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Add a delay to allow time for the page to load
                new_height = driver.execute_script(
                    "return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Scrape laptop data
            laptops = driver.find_elements(By.XPATH, '//div[@class="box--ujueT"]/div[@class="gridItem--Yd0sa"]')

            for laptop in laptops:
                # Extract the required laptop details
                info_div = laptop.find_element(By.XPATH, './/div[@class="info--ifj7U"]')
                name_element = info_div.find_element(By.XPATH, './/div[@class="title--wFj93"]/a')
                name = name_element.text
                link = name_element.get_attribute("href")
                price_element = info_div.find_element(By.XPATH, './/div[@class="price--NVB62"]/span')
                price = price_element.text

                try:
                    # Adjust rating out of 10
                    rating_element = info_div.find_element(By.XPATH, './/div[contains(@class, "rating--ZI3Ol")]')
                    rating_icons = rating_element.find_elements(By.XPATH, ".//i[contains(@class, 'star-icon--k88DV')]")
                    rating = 0
                    total_ratings = len(rating_icons)

                    for icon in rating_icons:
                        class_name = icon.get_attribute("class")
                        if "star-10" in class_name:
                            rating += 10
                        elif "star-9" in class_name:
                            rating += 9
                        elif "star-8" in class_name:
                            rating += 8
                        elif "star-7" in class_name:
                            rating += 7
                        elif "star-6" in class_name:
                            rating += 6
                        elif "star-5" in class_name:
                            rating += 5
                        elif "star-4" in class_name:
                            rating += 4
                        elif "star-3" in class_name:
                            rating += 3
                        elif "star-2" in class_name:
                            rating += 2
                        elif "star-1" in class_name:
                            rating += 1

                    if total_ratings > 0:
                        rating /= total_ratings
                    else:
                        rating = 0
                except NoSuchElementException:
                    rating = 0

                # Store the laptop details in a dictionary
                laptop_data = {
                    'Name': name,
                    'Price': price,
                    'Rating': rating,
                    'Link': link
                }
                data.append(laptop_data)

                # Store the laptop details into the database using Flask ORM
                existing_laptop = Laptop_Data.query.filter_by(laptopName=name).first()
                if existing_laptop is None:
                    # Store the laptop details in a new record
                    laptop_data = Laptop_Data(laptopName=name, laptopPrice=price, laptopRating=rating, laptopLink=link)
                    db.session.add(laptop_data)
                    db.session.commit()

                    # Serialize the laptop data using the schema
                    serialized_data = laptop_schema.dump([laptop_data])
                    json_data = jsonify(serialized_data)
                    # Perform any further processing or response handling with the JSON data


                else:
                    # Duplicate laptop entry found, skip adding to the database
                    logging.info(f"Skipping duplicate laptop entry: {name}")

                # Log the laptop details
                logging.info(f"Laptop Name: {name}, Price: {price}, Rating: {rating}")

            # Go to the next page
            next_page = driver.find_element(By.XPATH, '//li[@title="Next Page"]/a[@class="ant-pagination-item-link"]')
            actions = ActionChains(driver)
            actions.move_to_element(next_page).click().perform()


    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

# Schedule the bot to run every n days
def schedule_bot(day):
    schedule.every(day).days.do(scrape_laptop_data)
    while True:
        schedule.run_pending()
        time.sleep(1)

# scrape_laptop_data()