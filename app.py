import pygal, tempfile, webbrowser, os, csv
from lxml import etree
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy


#create a Flask object
app = Flask(__name__)

#allow the application to update while the server is running
app.config["DEBUG"] = True

#flash the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)