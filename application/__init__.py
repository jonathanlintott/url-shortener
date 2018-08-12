from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


app = Flask(__name__)

# Set config
app_settings = os.getenv(
    'APP_SETTINGS', 'application.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


import application.routes, application.models  # noqa
