import csv
from models import Connection

class Importer():
	conn = None
	ingredients = {}

	def __init__(self):
		self.conn = Connection()

	def import_ingredients(self):
		with open('ingredients.csv', 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			headers = []
			for i, row in enumerate(reader):
				# Build list of ingredients and skip to next row with matches
				if (i == 0):
					# Skip the first column cause it's empty
					for j in range(1, len(row)):
						self.ingredients[j] = {
							'name': row[j],
							'matches': []
						}
					continue

				# Get the ingredient for this row
				ingredient = row[0]

				print ingredient
				# Skip the first column cause it's the name of the ingredient
				for j in range(1, len(row)):
					strength = row[j]
					if (strength != ''):
						self.ingredients[j]['matches'].append(self.ingredients[i]['name'])
						print j, strength


			print self.ingredients



importer = Importer()
importer.import_ingredients()