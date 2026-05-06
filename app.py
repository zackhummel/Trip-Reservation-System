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
    return render_template('reservations.html')

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)