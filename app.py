import requests
import json
import datetime
from flask import Flask, request

app = Flask(__name__)

# Import models and create tables
from models import *


@app.route('/')
def home():
	model = Ingredient()
	ingredients = model.get_all()
	return ingredients


@app.route('/ingredient', methods=['POST'])
def createIngredient():
	return 'fuck'


@app.route('/ingredient/connection', methods=['POST'])
def createIngredientConnection():
	return 'shit'


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')

