# config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hotel_pms.db')  # Database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
