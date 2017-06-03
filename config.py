import os

class Config(object):
	SECRET_KEY = os.environ['SECRET_KEY']
	DEBUG = os.environ['DEBUG']
	DB_NAME = 'postgres'
	DB_USER = os.environ['DB_USER']
	DB_PASS = os.environ['DB_PASS']
	DB_HOST = os.environ['DB_HOST']
	DB_PORT = os.environ['DB_PORT']
	SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
		DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
	)