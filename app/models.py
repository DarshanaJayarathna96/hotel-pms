# app/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    room_number = db.Column(db.String(10), nullable=False)  # Column for room number
    payment_status = db.Column(db.String(10), nullable=False, default="Unpaid")  # Payment status
    amount_due = db.Column(db.Float, nullable=False)  # Amount due
    confirmation_number = db.Column(db.String(20), nullable=False, unique=True)  # Unique confirmation number

    def __repr__(self):
        return f'<Guest {self.first_name} {self.last_name}>'
