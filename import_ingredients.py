import csv
from models import Connection
import datetime

class Importer():
	conn = None
	ingredients = {}

	_columns_to_skip = 1

	def __init__(self):
		self.conn = Connection()

	def get_ingredients(self):
		self.conn.cursor.execute('SELECT id, name FROM ingredients')
		self.conn.connection.commit()

		ingredients = {}
		for i in self.conn.cursor.fetchall():
			# print i
			ingredients[i['name']] = i['id']
		
		return ingredients

	def parse_file(self):
		with open('ingredients.csv', 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			headers = []
			for i, row in enumerate(reader):
				# Build list of ingredients and skip to next row with matches
				if (i == 0):
					# Skip n columns
					for j in range(self._columns_to_skip, len(row)):
						self.ingredients[j] = {
							'name': row[j],
							'matches': {}
						}
					continue

				# Skip n columns
				for j in range(self._columns_to_skip, len(row)):
					strength = row[j]
					if (strength != ''):
						self.ingredients[j]['matches'][self.ingredients[i]['name']] = strength


	def import_ingredients(self):
		self.parse_file()

		# First loop over and import all the ingredients
		for i in self.ingredients:
			ingredient = self.ingredients[i]
			self.conn.cursor.execute('INSERT INTO ingredients (name, created_at) VALUES (%s, %s) ON CONFLICT DO NOTHING', (ingredient['name'], datetime.datetime.now(),))
		self.conn.connection.commit()

		# Then select all ingredients from the DB so we have their IDs
		ingredients_map = self.get_ingredients()

		# Insert all connections
		for i, ingredient in self.ingredients.iteritems():
			query = 'INSERT INTO ingredient_connections (ingredient1,ingredient2, strength) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING'
			
			ingredient1 = ingredients_map[ingredient['name']]
			for name, strength in ingredient['matches'].iteritems():
				ingredient2 = ingredients_map[name]
				
				self.conn.cursor.execute(query, (ingredient1, ingredient2, strength))

		
		self.conn.connection.commit()



importer = Importer()
importer.import_ingredients()