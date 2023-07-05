import os
from flask import Flask, render_template
from flask_cors import CORS
from datetime import timedelta, datetime

app = Flask(__name__)
app.secret_key = "codeaza-project"
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/codeaza_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)


from Scrape_Data import models

# Create the database tables
with app.app_context():
    models.db.create_all()

# Import views after creating the tables
from Scrape_Data import views
