from config import Config
import datetime
import json
from marshmallow import Schema, fields
from sqlalchemy.ext.declarative import declarative_base as real_declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker

# Create engine and session
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

declarative_base = lambda cls: real_declarative_base(cls=cls)

def datetime_handler(x):
	if isinstance(x, datetime.datetime):
		return x.isoformat()

@declarative_base
class Base(object):
	

	# @property
	# def columns(self):
	# 	return [ c.name for c in self.__table__.columns ]

	# @property
	# def columnitems(self):
	# 	return dict([ (c, self[c]) for c in self.columns ])

	@property
	def tojson(self):
		return json.dumps(self.__dict__, default=datetime_handler)



# Define classes
class Ingredient(Base):
	__tablename__ = 'ingredients'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	created_at = Column(DateTime, nullable=False)

	def __init__(self, name):
		self.name = name
		self.created_at = datetime.datetime.now()


class IngredientSchema(Schema):
	name = fields.Str()
	created_at = fields.DateTime()


class IngredientConnections(Base):
	__tablename__ = 'ingredient_connections'

	ingredient1 = Column(Integer, primary_key=True)
	ingredient2 = Column(Integer, primary_key=True)
	strength = Column(Integer, nullable=False)

	def __init__(self, ingredient1, ingredient2, strength=1):
		self.ingredient1 = ingredient1
		self.ingredient2 = ingredient2
		self.strength = strength