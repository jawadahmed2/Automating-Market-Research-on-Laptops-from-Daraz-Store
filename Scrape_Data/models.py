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

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName','lastName','userName','email','password')

# db.create_all()