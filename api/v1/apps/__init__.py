from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from config import ConfigClass

app = Flask(__name__)
app.config.from_object(ConfigClass)

# Load local_settings.py if file exists
try: app.config.from_object('local_settings')
except: pass

db = SQLAlchemy(app)

api = Api(app, app.config['APPLICATION_ROOT'])
from apps.urls import add_resource
add_resource()
