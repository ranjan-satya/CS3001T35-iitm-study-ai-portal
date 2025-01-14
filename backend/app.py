from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import JWTManager
import os
from flasgger import Swagger

from os.path import basename
from flask.globals import g
from os.path import isfile
from flask.cli import with_appcontext
import sqlite3
from sqlite3 import dbapi2 as sqlite
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
# Set the path to the database file
database_file = os.path.join(current_directory, "iitdatabase.db")

# Configure the Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database_file + "?charset=utf8"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': {'detect_types': sqlite.PARSE_DECLTYPES | sqlite.PARSE_COLNAMES}}
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['DEBUG'] = True

db = SQLAlchemy(app)
CORS(app)
jwt = JWTManager(app)
swagger = Swagger(app, template_file='api.yaml')

from routes import *
from model import *

if __name__ == '__main__':
    app.run(port=5000)
