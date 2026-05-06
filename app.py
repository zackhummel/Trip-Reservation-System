import pygal, tempfile, webbrowser, os, csv, sqlite3
from lxml import etree
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy



#create a Flask object
app = Flask(__name__)

#allow the application to update while the server is running
app.config["DEBUG"] = True

#flash the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    try:
        #connect to the reservations.db database
        conn = sqlite3.connect('reservations.db')
        #set the row factory to sqlite3.Row to access columns by name
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def get_reservationID(code):
    #get a connection to the database
    mydb = get_db_connection()
    cursor = mydb.cursor()
    query = 'SELECT * FROM reservations WHERE id = ?;'
    cursor.execute(query, (code,))
    reservationID = cursor.fetchone()
    return reservationID

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        menu_choice = request.form.get('menu_option')

        if menu_choice == "admin":
            return redirect(url_for('admin'))
        elif menu_choice == "create":
            return redirect(url_for('create_reservation_get'))
        else:
            flash('Please select an option.', 'error')
            return redirect(url_for('index'))
        
    return render_template('index.html')



@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():
    mydb = get_db_connection()
    cursor = mydb.cursor()
    query = "SELECT * FROM reservations;"
    cursor.execute(query)
    reservations = cursor.fetchall()

    
    return render_template('reservations.html', reservations=reservations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
        mydb = get_db_connection()
        cursor = mydb.cursor()
        query = "SELECT * FROM admins WHERE username = ? AND password = ?;"
        cursor.execute(query, (username, password))
        admin = cursor.fetchone()

        mydb.close()
        if admin: 
            flash('Login successful!', 'success')
            return redirect(url_for('reservations'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return render_template('admin.html')
        
    return render_template('admin.html')

@app.route('/<code>/delete/', methods=('GET',))
def delete_get(code):

    reservationID = get_reservationID(code)
    return render_template('delete.html', reservationID=reservationID)

@app.route('/<code>/delete/', methods=('POST',))
def delete_post(code):
    #get a connection to the database and create a cursor
    mydb = get_db_connection()
    cursor = mydb.cursor()

    #create and execute a query to delete the reservation with the reservation id that was passed as a url parameter
    delete_query = 'DELETE FROM reservations WHERE id = ?;'
    cursor.execute(delete_query, (code,))
    mydb.commit()
    mydb.close()

    #redirect to the homepage
    return redirect(url_for('index'))

@app.route('/create', methods=('GET',))
def create_reservation_get():
    return render_template('createReservation.html')
@app.route('/create', methods=('POST',))
def create_reservation_post():
    #connect to the database and create a cursor 
    mydb = get_db_connection()
    cursor = mydb.cursor()
    #get form data
    passengerName = request.form.get('firstname')
    lastName = request.form.get('lastname')
    seatRow = request.form.get('row')
    seatColumn = request.form.get('seat')
    #validate all required fields are submitted
    error_message = ""

    if not passengerName:
        error_message += "\nFirstname required. "
    if not lastName:
        error_message += "\nLastname required. "
    if not seatRow:
        error_message += "\nRow required. "
    if not seatColumn:
        error_message += "\nSeat is required. "
     
        
    if error_message: 
        flash(error_message)
        return redirect(url_for('create_reservation_get'))
    #create an insert query
    insert_query = "INSERT INTO reservations (passengerName, seatRow, seatColumn) values  (?, ?, ?, ?);"
    #execute the query and check for errors
    try:
        cursor.execute(insert_query, (passengerName, seatRow, seatColumn))
        mydb.commit()

        if cursor.rowcount == 0:
            flash(f"ERROR: Reservation for {passengerName} was not created")
            return redirect(url_for('create_reservation_get'))
        else: 
            flash(f"SUCCESS: {cursor.rowcount} new reservation(s) created.\nSee results below")

    except sqlite3.Error as e:
        flash(f"Database error: {e}")
        return redirect(url_for('create_reservation_get'))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)