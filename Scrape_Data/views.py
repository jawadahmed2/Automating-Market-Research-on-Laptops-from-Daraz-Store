import json
from numpy import tile
from requests import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort, redirect, render_template, jsonify, request, url_for
from .models import User, UserSchema, Product_Reviews, Product_ReviewsSchema,Laptop_Data, Laptop_DataSchema, db
from .scrapeReviews import getdata, parse_html, get_cus_names, get_cus_reviews, reviews_in_json, make_dataframe, wordCloud, getTitle
from urllib.parse import urlparse
from sqlalchemy.exc import SQLAlchemyError
from .scrapeLaptopData import scrape_laptop_data
from Scrape_Data import app

user_schema = UserSchema()
user_schema = UserSchema(many=True)

product_review_schema = Product_ReviewsSchema()
product_review_schema = Product_ReviewsSchema(many=True)

laptop_schema = Laptop_DataSchema()
laptop_schema = Laptop_DataSchema(many=True)

@app.route('/')
def index():
    return 'Server Is Active. Access its Services Through Client or Frontend'

@app.route('/home')
def home():
    # Retrieve the laptop data from the database
    laptop_data = Laptop_Data.query.all()

    # Serialize the laptop data using the schema
    serialized_data = laptop_schema.dump(laptop_data)

    # Return the JSON data to the home.html template
    return jsonify(serialized_data)

@app.route('/startsraping/api', methods=['GET'])
def startscraping():
    # Call the scrapeLaptopData function to start the scraping process
    print('Request Made To Start Scraping')
    scrape_laptop_data()

    # Return a response indicating the scraping process has started
    return "Scraping process started"



@app.route("/registration/api", methods=["POST"])
def registration():
    fName = request.json['fname']
    lName = request.json['lname']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if fName and email and lName and username and password:
        encrypted_password = generate_password_hash(password)
        registration_items = User(
            fName, lName, username, email, encrypted_password)
        success = 'User Successfully Added In The Database '
        query = User.query.all()
        result = user_schema.dump(query)
        if len(result) == 0:
            print('Success')
            try:
                db.session.add(registration_items)
                db.session.commit()
                return jsonify({'name': success})
            except SQLAlchemyError as e:
                db.session.rollback()
                error_msg = str(e.__class__.__name__) + ": " + str(e)
                return jsonify({'error': error_msg})

        flag = any(obj['email'] == email for obj in result)
        if flag:
            return jsonify({'error': 'Email already exists. Kindly login.'})
        print('Successfully Added')
        try:
            db.session.add(registration_items)
            db.session.commit()
            return jsonify({'name': success})
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = str(e.__class__.__name__) + ": " + str(e)
            return jsonify({'error': error_msg})

    return jsonify({'error': 'Missing data! Kindly Fill All Entries.'})



@app.route("/login/api", methods=["POST"])
def login():
    email = request.json['email']
    password = request.json['password']
    if email and password:
        query = User.query.all()
        result = user_schema.dump(query)
        flag = any(obj['email'] == email for obj in result)
        if flag:
            print('User Exist')
            success = 'Successfully Login '
            session['loggedin'] = 'loggedin'
            for obj in result:
                if check_password_hash(obj['password'], password):
                    # session['loggedin'] = 'loggedin'
                    # session['id'] = obj['id']
                    # session['email'] = obj['email']
                    if email == 'jawad2019@namal.edu.pk':
                        return jsonify({'name': success, 'user': 'admin'})
                    return jsonify({'name': success, 'user': 'user'})

        return jsonify({'error': 'Email is not registered. Kindly register.'}) if flag else jsonify({'error': 'Email Or Password Is Wrong.'})

    return jsonify({'error': 'Missing data! Kindly Fill All Entries.'})


@app.route('/logout/api', methods=['POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return jsonify({'logout': 'home'})


@app.route('/scrapeReviewsGuest/api', methods=['POST'])
def guestscrapeReviews():
    if urlparse(request.form['url']).netloc == 'www.daraz.pk':
        product_url = request.form['url']
        # Parse Product data
        parse_product = parse_html(product_url)
        # Getting the customer names
        names = get_cus_names(parse_product)

        if len(names) > 0:
            # names.pop(0)
            cus_names = []  # Finalize the customer names
            # Remove the duplicates
            [cus_names.append(x) for x in names if x not in cus_names]

            # Get the reviews data
            rev_data = get_cus_reviews(parse_product)
            title = getTitle(parse_product)

            if title is not None:
                title_value = title.string
            else:
                title_value = "Unknown"

            # Convert the customer names and their reviews into JSON
            get_json_reviews = json.loads(reviews_in_json(cus_names, rev_data, title_value))

            print('Successfully Scraped Product Reviews')
            # frequent_words = wordCloud(make_dataframe(cus_names, rev_data))
            # print(frequent_words)
            return jsonify(get_json_reviews)

    return jsonify({'error': 'Missing data! OR Invalid Daraz Product Link!'})





@app.route('/scrapeReviewsUser/api', methods=['POST'])
def scrapeReviewsUser():
    # if 'loggedin' not in session:
    #     return redirect(url_for('guestscrapeReviews'))
    if urlparse(request.form['url']).netloc != 'www.amazon.com':
        return jsonify({'error': 'Missing data! OR Invalid Amazon Product Link!'})

    product_url = request.form['url']
    # Parse Product data
    parse_product = parse_html(product_url)
    # getting the customer names
    names = get_cus_names(parse_product)
    names.pop(0)
    cus_names = []  # finalize the customer names
    # remove the dublicates
    [cus_names.append(x) for x in names if x not in cus_names]
    # Get the reviews data
    rev_data = get_cus_reviews(parse_product)
    title = getTitle(request.form['url'])
    # convert the customer names and its reviews into json
    get_json_reviews = json.loads(
        reviews_in_json(cus_names, rev_data, title))
    print('Successfully Scraped Product Reviews')
    frequent_words = wordCloud(make_dataframe(cus_names, rev_data))
    # print(frequent_words)

    # print(get_json_reviews)
    try:
        reviews_items = Product_Reviews(title, json.dumps(
            get_json_reviews), ' '.join(str(item) for item in frequent_words))
        db.session.add(reviews_items)
        db.session.commit()
    except ValueError:
        print("Values Not Store In The Database")

    # Id = session['id']
    # print(Id)
    return jsonify(get_json_reviews)


@app.route('/scrapeFrequentWords/api', methods=['POST'])
def scrapeFrequentWords():
    # if 'loggedin' not in session:
    #     return redirect(url_for('guestscrapeReviews'))
    if urlparse(request.form['url']).netloc != 'www.amazon.com':
        return jsonify({'error': 'Missing data! OR Invalid Amazon Product Link!'})

    product_url = request.form['url']
    # Parse Product data
    parse_product = parse_html(product_url)
    # getting the customer names
    names = get_cus_names(parse_product)
    names.pop(0)
    cus_names = []  # finalize the customer names
    # remove the dublicates
    [cus_names.append(x) for x in names if x not in cus_names]
    # Get the reviews data
    rev_data = get_cus_reviews(parse_product)
    print('Successfully Scraped Product Reviews')
    frequent_words = wordCloud(make_dataframe(cus_names, rev_data))
    words = dict(enumerate(frequent_words))
    print(words)
    return jsonify(words)

@app.route("/adminHome/api", methods=["GET"])
def get_user_length():
    items = User.query.all()
    result = user_schema.dump(items)
    length = len(result)
    return jsonify({'length': length})

@app.route("/adminUser/api", methods=["GET"])
def get_user_details():
    items = User.query.all()
    result = user_schema.dump(items)
    return jsonify(result)

@app.route("/showProducts/api", methods=["GET"])
def get_product_details():
    items = Product_Reviews.query.all()
    result = product_review_schema.dump(items)
    print(result)
    return jsonify(result)

@app.route("/userDelete/api/<id>", methods=["GET"])
def delete_user(id):
    if user := User.query.get(id):
        db.session.delete(user)
        db.session.commit()
        return user_schema.jsonify(user)

    return abort(404)