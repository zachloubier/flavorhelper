from config import Config
import datetime
import json
import psycopg2 as pg2
import psycopg2.extras

def datetime_handler(x):
	if isinstance(x, datetime.datetime):
		return x.isoformat()

class Connection():
	connection = None
	cursor = None

	def __init__(self):
		self.connection = pg2.connect(
			dbname=Config.DB_NAME,
			user=Config.DB_USER,
			password=Config.DB_PASS,
			host=Config.DB_HOST,
			port=Config.DB_PORT
		)
		self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

	def query(self, sql, binds=None):
		self.cursor.execute(sql, (binds,))
		return self.cursor

class BaseModel():
	__tablename__ = ''
	_pk = 'id'
	conn = None

	def __init__(self):
		self.conn = Connection()

	def get(self, id, as_json=True):
		query = 'SELECT * FROM {0} WHERE {1} = %s'.format(self.__tablename__, self._pk)

		row = self.conn.query(query, id).fetchone()
		if (as_json):
			row = self.to_json(row)
		
		return row

	def get_all(self, as_json=True):
		query = 'SELECT * FROM {0}'.format(self.__tablename__)

		rows = self.conn.query(query).fetchall()
		if (as_json):
			rows = self.to_json(rows)

		return rows

	def to_json(self, result):
		return json.dumps(result, default=datetime_handler)


# Define classes
class Ingredient(BaseModel):
	__tablename__ = 'ingredients'
	_pk = 'id'


class IngredientConnections(BaseModel):
	__tablename__ = 'ingredient_connections'
	_pk = 'ingredient1'



	# def __init__(self, ingredient1, ingredient2, strength=1):
	# 	self.ingredient1 = ingredient1
	# 	self.ingredient2 = ingredient2
	# 	self.strength = strength