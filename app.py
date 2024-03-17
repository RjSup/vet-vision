from flask import (
    Flask,
    redirect,
    request,
    render_template,
    g,
    url_for,
    session
)

import os
import sqlite3 as sql
from dotenv import load_dotenv

# Load the .env file from root directory
load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_CODE')

# database name
db_pets = "pets.db"
db_login = "logins.db"


# Connect to our databse
def get_pet_db():
    # Gets a database connection, creating one if needed
    if 'db' not in g:
        g.db = sql.connect(db_pets)
    return g.db


def get_login_db():
    if 'db' not in g:
        g.db = sql.connect(db_login)
    return g.db


# Close the connection of the databse
@app.teardown_appcontext
def close_connection(exception):
    # Closes the database connection at the end of the request
    db = g.pop('db', None)
    if db is not None:
        db.close()


def check_credentials(username, password):
    con = sql.connect("logins.db")
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    con.close()
    return user is not None


# handles the login page and logic for login in
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_credentials(username, password):
            session['logged_in'] = True
            return redirect(url_for('all_pets'))
        else:
            # Display an error message for incorrect credentials
            return "Error with these credentials"
    else:
        return render_template('login.html')


# landing page - handling form data and storing in database
# TODO Remove form data after submission - Add login to database button and login process
@app.route('/', methods=['GET', 'POST'])
def add_pet():
    # If a GET request - go to the landing page
    if request.method == 'GET':
        return render_template("index.html")
    # if a POST request - take the data from the forms and add to the database
    elif request.method == 'POST':
        owner_name = request.form["owner_name"]
        pet_name = request.form["pet_name"]
        pet_type = request.form["pet_type"]
        pet_id = request.form["pet_id"]

        # Get a database connection within the route context
        db = get_pet_db()
        cursor = db.cursor()

        with open("schema.sql", "r") as f:  # Open schema file within the route
            cursor.executescript(f.read())  # Create schema if needed

        # Insert data into the table
        cursor.execute(
            "INSERT INTO pets (owner_name, pet_name, pet_type, pet_id) VALUES(?, ?, ?, ?)",
            (owner_name, pet_name, pet_type, pet_id)
        )
        db.commit()

        return "Pet added successfully!"
    

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # If a GET request - go to the landing page
    if request.method == 'GET':
        return render_template("contact.html")


# Database page handles checking the database and removing data
@app.route('/all_pets', methods=['GET', 'POST'])
def all_pets():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    db = get_pet_db()
    cursor = db.cursor()

    # If a GET request - retrieve all pets from database
    if request.method == 'GET':
        cursor.execute("SELECT * FROM pets")
        pets = cursor.fetchall()
        return render_template("all_pets.html", pets=pets)

    # If a POST request - remove specific items from database
    elif request.method == 'POST':
        owner_name_delete = request.form.get("owner_name_delete")
        pet_name_delete = request.form.get("pet_name_delete")
        pet_type_delete = request.form.get("pet_type_delete")
        pet_id = request.form.get("pet_id")

        try:
            query = "DELETE FROM pets WHERE "
            conditions = []
            if owner_name_delete:
                conditions.append("owner_name = ?")
            if pet_name_delete:
                conditions.append("pet_name = ?")
            if pet_type_delete:
                conditions.append("pet_type = ?")
            if pet_id:
                conditions.append("pet_id = ?")
            query += " AND ".join(conditions)

            parameters = tuple([escape_input(val) for val in (
                owner_name_delete, pet_name_delete, pet_type_delete, pet_id) if val])
            cursor.execute(query, parameters)
            db.commit()

            return redirect(url_for('all_pets'))
        except sql.Error as e:
            return f"An error occurred: {e}", 500

# TODO Need to implement a robust escape_input function for security


def escape_input(value):
    # Properly escape user-provided input to preven
    # Consider using built-in escaping mechanisms or libraries
    return value  # Replace with actual escaping logic


if __name__ == '__main__':
    app.run()
