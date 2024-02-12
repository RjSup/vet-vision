from flask import Flask, request, render_template, g
import sqlite3

app = Flask(__name__)

# Database name
db_name = "pets.db"

def get_db():
    """Gets a database connection, creating one if needed."""
    if 'db' not in g:
        g.db = sqlite3.connect(db_name)
    return g.db


@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/', methods=["GET", "POST"])
def add_pet():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        owner_name = request.form["owner_name"]
        pet_name = request.form["pet_name"]
        pet_type = request.form["pet_type"]

        # Get a database connection within the route context
        db = get_db()
        cursor = db.cursor()

        with open("schema.sql", "r") as f:  # Open schema file within the route
            cursor.executescript(f.read())  # Create schema if needed

        # Insert data into the table
        cursor.execute(
            "INSERT INTO pets (owner_name, pet_name, pet_type) VALUES (?, ?, ?)",
            (owner_name, pet_name, pet_type),
        )
        db.commit()

        return "Pet added successfully!"
    

@app.route('/all_pets')
def all_pets():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    return render_template("all_pets.html", pets=pets)


if __name__ == '__main__':
    app.run()
