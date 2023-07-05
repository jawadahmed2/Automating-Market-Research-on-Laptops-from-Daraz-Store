from Scrape_Data import app
import json
from requests import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort, redirect, render_template, jsonify, request, url_for
from .models import User, UserSchema, db
user_schema = UserSchema()
user_schema = UserSchema(many=True)



@app.route('/')
def index():
    return 'Server Is Active. Access its Services Through Client or Frontend'

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
            db.session.add(registration_items)
            db.session.commit()
            return jsonify({'name': success})

        flag = any(obj['email'] == email for obj in result)
        if flag:
            return jsonify({'error': 'Email already exists. Kindly login.'})
        print('Successfully Added')
        db.session.add(registration_items)
        db.session.commit()
        return jsonify({'name': success})

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