import json
from flask import  jsonify, request
from .models import  Laptop_Data, Laptop_DataSchema, db
from .scrapeLaptopData import scrape_laptop_data
from Scrape_Data import app


laptop_schema = Laptop_DataSchema()
laptop_schema = Laptop_DataSchema(many=True)


@app.route('/')
def index():
    return 'Server Is Active. Access its Services Through Client or Frontend'


@app.route('/home/api')
def home():
    # Retrieve the laptop data from the database
    laptop_data = Laptop_Data.query.all()

    # Serialize the laptop data using the schema
    serialized_data = laptop_schema.dump(laptop_data)

    # Return the JSON data to the home.html template
    return jsonify(serialized_data)


@app.route('/get-total-laptop-data/api', methods=['GET'])
def get_total_laptop_data():
    # Calculate the total number of laptop data
    total_laptop_data = Laptop_Data.query.count()

    # Create a JSON response
    response = {
        'total': total_laptop_data
    }

    # Return the response
    return jsonify(response)


@app.route('/startsraping/api', methods=['POST'])
def startscraping():
    num_pages = int(request.form['numPages'])

    # Call the scrapeLaptopData function to start the scraping process
    print(f"Request Made To Start Scraping with num_pages: {num_pages}")
    scrape_laptop_data(num_pages)  # Enter number of pages to scrape

    # Return a response indicating the scraping process has started
    return "Scraping process started"


@app.route('/scrapeReviews/api', methods=['POST'])
def guestscrapeReviews():
   pass