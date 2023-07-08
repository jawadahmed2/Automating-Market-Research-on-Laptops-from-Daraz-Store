from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from numpy import rec


from Scrape_Data import app

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120))
    lastName = db.Column(db.String(120))
    userName = db.Column(db.String(120))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __init__(self, firstName,lastName,userName,email,password):
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.email = email
        self.password = password

class Product_Reviews(db.Model):
    __tablename__ = 'product_reviews'
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.Text())
    productReviews = db.Column(db.Text())
    frequentWords = db.Column(db.Text())
    recommendation = db.Column(db.String(100))

    def __init__(self, productName,productReviews,frequentWords):
        self.productName = productName
        self.productReviews = productReviews
        self.frequentWords = frequentWords

class Laptop_Data(db.Model):
    __tablename__ = 'laptop_data'
    id = db.Column(db.Integer, primary_key=True)
    laptopName = db.Column(db.Text())
    productReviews = db.Column(db.Text())
    frequentWords = db.Column(db.Text())
    recommendation = db.Column(db.String(100))

    def __init__(self, productName,productReviews,frequentWords):
        self.productName = productName
        self.productReviews = productReviews
        self.frequentWords = frequentWords

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName','lastName','userName','email','password')

class Product_ReviewsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'productName','productReviews','frequentWords')

# db.create_all()