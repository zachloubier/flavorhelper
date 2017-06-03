import requests
import json
import datetime
import psycopg2 as pg2
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)


# Import models and create tables
from models import *
Base.metadata.create_all(engine)


def datetime_handler(x):
	if isinstance(x, datetime.datetime):
		return x.isoformat()
	# raise TypeError("Unknown Type")


@app.route('/')
def home():
	# Get all ingredients
	session = Session()
	allIngredients = session.query(Ingredient).order_by(Ingredient.name).all()

	schema = IngredientSchema()
	response = []
	for row in allIngredients:
		response.append(schema.dump(row))

	# return json.dumps(response, default=datetime_handler)



	return json.dumps(response)


@app.route('/ingredient', methods=['POST'])
def createIngredient():
	data = request.form

	ingredient = Ingredient(name=data['name'])

	session.add(ingredient)
	session.commit()


@app.route('/ingredient/connection', methods=['POST'])
def createIngredientConnection():
	data = request.form

	# Create connection
	conn = IngredientConnections(ingredient1=data.ingredient1, ingredient2=data.ingredient2)
	session.add(conn)
	session.commit()


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')

