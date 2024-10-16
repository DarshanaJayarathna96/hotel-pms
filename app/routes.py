from flask import render_template, request, abort
from . import db
from .models import Guest
from datetime import datetime
import uuid

def generate_confirmation_number():
    return str(uuid.uuid4())[:8]

def register_routes(app):
    @app.route('/')
    def index():
        print('aa')  # Just for debugging purposes
        return render_template('index.html')

    @app.route('/add_guest', methods=['POST'])
    def add_guest():
        # Collect form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        room_number = request.form['room_number']  # Add room number from form
        amount_due = request.form['amount_due']  # Add amount due from form

        # Convert check-in and check-out to date objects
        check_in = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out, '%Y-%m-%d').date()

        # Generate confirmation number
        confirmation_number = generate_confirmation_number()

        # Create a new Guest instance
        new_guest = Guest(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            check_in=check_in,
            check_out=check_out,
            room_number=room_number,
            amount_due=amount_due,
            confirmation_number=confirmation_number
        )

        # Add the new guest to the session and commit to the database
        db.session.add(new_guest)
        db.session.commit()

        # Redirect to index with confirmation number
        return render_template('confirmation.html', confirmation_number=confirmation_number)

    @app.route('/checkout/<int:guest_id>', methods=['POST'])
    def checkout(guest_id):
        guest = Guest.query.get_or_404(guest_id)

        # Mark payment status as paid
        guest.payment_status = 'Paid'
        db.session.commit()

        # Generate an invoice
        return render_template('invoice.html', guest=guest)

    @app.route('/guests', methods=['GET'])
    def get_guests():
        guests = Guest.query.all()  # Query all guests from the database
        return render_template('guest_table.html', guests=guests)

    @app.route('/invoice/<confirmation_number>')
    def invoice(confirmation_number):
        guest_data = get_guest_data(confirmation_number)

        if guest_data is None:
            # Handle case where no guest is found with that confirmation number
            return abort(404)  # Return a 404 error if not found

        return render_template('invoice.html', guest=guest_data)

    def get_guest_data(confirmation_number):
        # Query the database for the guest with the given confirmation number
        guest = Guest.query.filter_by(confirmation_number=confirmation_number).first()

        if guest:  # If a guest is found, return their data
            return {
                "first_name": guest.first_name,
                "last_name": guest.last_name,
                "room_number": guest.room_number,
                "check_in": guest.check_in,
                "check_out": guest.check_out,
                "amount_due": guest.amount_due,
                "payment_status": guest.payment_status,
                "confirmation_number": guest.confirmation_number
            }
        else:  # If no guest is found, return None or handle it as needed
            return None
