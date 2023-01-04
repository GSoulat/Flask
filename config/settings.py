import os
from dotenv import load_dotenv

load_dotenv(override=True)

class BaseConfig():
   API_PREFIX = '/api'
   TESTING = False
   DEBUG = False


class DevConfig(BaseConfig):
   FLASK_ENV = 'development'
   DEBUG = True
   SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
   SECRET_KEY = 'myclefsecret'
   SQLALCHEMY_TRACK_MODIFICATIONS = True
   APPINSIGHTS_INSTRUMENTATIONKEY = os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")
   GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
   GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


class ProductionConfig(BaseConfig):
   FLASK_ENV = 'production'
   SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace('postgres://','postgresql://')
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   SECRET_KEY = 'myclefsecret'
   APPINSIGHTS_INSTRUMENTATIONKEY = os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")
   GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
   GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

class TestConfig(BaseConfig):
   FLASK_ENV = 'development'
   TESTING = True
   DEBUG = True