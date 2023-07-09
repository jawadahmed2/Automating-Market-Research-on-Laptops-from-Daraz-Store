from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from Scrape_Data import app

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Laptop_Data(db.Model):
    __tablename__ = 'laptop_data'
    id = db.Column(db.Integer, primary_key=True)
    laptopName = db.Column(db.Text())
    laptopPrice = db.Column(db.Text())
    laptopRating = db.Column(db.Text())

    def __init__(self, laptopName, laptopPrice, laptopRating):
        self.laptopName = laptopName
        self.laptopPrice = laptopPrice
        self.laptopRating = laptopRating



class Laptop_DataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'laptopName','laptopPrice','laptopRating')

