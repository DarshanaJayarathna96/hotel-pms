# app/__init__.py

from flask import Flask

from config import Config
from .models import db  # Import db from models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)  # Initialize SQLAlchemy with the app

    with app.app_context():
        db.create_all()  # Create all database tables

        from . import routes  # Import routes after creating the app context
        routes.register_routes(app)  # Register your routes

    return app
