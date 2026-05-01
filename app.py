import pygal, tempfile, webbrowser, os, csv
from lxml import etree
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#create a Flask object
app = Flask(__name__)

#allow the application to update while the server is running
app.config["DEBUG"] = True

#flash the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/database/reservations.db'
db = SQLAlchemy(app)


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    passengerName = db.Column(db.String, nullable=False)
    seatRow = db.Column(db.Integer, nullable=False)
    seatColumn = db.Column(db.Integer, nullable=False)
    eTicketNumber = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        menu_choice = request.form.get('menu_option')

        if menu_choice == "admin":
            return redirect(url_for('admin'))
        elif menu_choice == "reserve":
            return redirect(url_for('reservations'))
        else:
            flash('Please select an option.', 'error')
            return redirect(url_for('index'))
        
    return render_template('index.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():
    toEncode = "INFOTC4320"

    if request.method == 'POST':
        firstName = request.form.get('fname')
        lastName = request.form.get('lname')
        
        selected_row = int(request.form.get('selectedRow'))
        selected_seat = int(request.form.get('selectedSeat'))

        existing = Reservation.query.filter_by(seatRow=selected_row, seatColumn=selected_seat).first()

        if firstName.strip() == "" or lastName.strip() == "":
            flash('Please enter a valid name.', 'error')
        elif selected_row == None:
            flash('Please select a row.', 'error')
        elif selected_seat == None:
            flash('Please select a seat.', 'error')
        elif existing:
            flash('Seat already filled, please pick a different seat.', 'error')
        else:
            encoded = ""
            for i in range(max(len(firstName), len(toEncode))):
                if i < len(firstName):
                    encoded += firstName[i]
                if i < len(toEncode):
                    encoded += toEncode[i]

            newRes = Reservation(
                passengerName = firstName,
                seatRow = selected_row,
                seatColumn = selected_seat,
                eTicketNumber = encoded
            )

            db.session.add(newRes)
            db.session.commit()

            flash(f"Congradulations {firstName}! Row: {selected_row}; Seat: {selected_seat} is now reserved for you! Your eticket number is: {encoded}")

    all_reservations = Reservation.query.all()

    seatsOnly = [(r.seatRow, r.seatColumn) for r in all_reservations]

    return render_template('reservations.html', takenSeats = seatsOnly)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)