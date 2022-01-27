# wsgi.py
# pylint: disable=missing-docstring
BASE_URL = '/api/v1'    #création de l' API

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow  # NEW LINE (L'ordre est important ici !)
from math import prod
from flask import Flask, request
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)  # NEW LINE
migrate = Migrate(app, db)

from models import Product
from schemas import many_product_schema, one_product_schema   #création de l' API

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200

@app.route(f'{BASE_URL}/products', methods=['GET', 'POST'])
def get_many_product():
    if request.method == 'GET':
        products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
        return many_product_schema.jsonify(products), 200
    elif request.method == 'POST':
        product = request.get_json()
        prod1 = Product(name=product['name'], description=product['description'])
        db.session.add(prod1)
        db.session.commit()
        products = db.session.query(Product).all()
        return many_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def get_one_product(id):
    if request.method == 'GET':
        ids = id if int(id) is not None else 0
        product = db.session.query(Product).get(int(ids))
        return one_product_schema.jsonify(product), 200
    if request.method == 'DELETE':
        ids = id if int(id) is not None else 0
        product = db.session.query(Product).get(int(ids))
        db.session.delete(product)
        db.session.commit()
        products = db.session.query(Product).all()
        return many_product_schema.jsonify(products), 200
    elif request.method == 'PATCH':
        ids = id if int(id) is not None else 0
        product = db.session.query(Product).get(int(ids))
        product_request = request.get_json()
        product.name = product_request['name']
        product.description=product_request['description']
        db.session.commit()
        products = db.session.query(Product).all()
        return many_product_schema.jsonify(products), 200
    
