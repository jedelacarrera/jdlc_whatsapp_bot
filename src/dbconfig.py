import os
from flask_sqlalchemy import SQLAlchemy
from app import app

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy configuration
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # silence the deprecation warning
db = SQLAlchemy(app)
