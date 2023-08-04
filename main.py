from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# SQLite Database Setup
import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def populate_inventory():
    items = [
        ("Item 1", random.randint(1, 100), random.uniform(1.0, 100.0)),
        ("Item 2", random.randint(1, 100), random.uniform(1.0, 100.0)),
        ("Item 3", random.randint(1, 100), random.uniform(1.0, 100.0)),
        ("Item 4", random.randint(1, 100), random.uniform(1.0, 100.0)),
        ("Item 5", random.randint(1, 100), random.uniform(1.0, 100.0)),
        ("Item 6", random.randint(1, 100), random.uniform(1.0, 100.0)),
        ("Item 7", random.randint(1, 100), random.uniform(1.0, 100.0)),
        ("Item 8", random.randint(1, 100), random.uniform(1.0, 100.0)),
        ("Item 9", random.randint(1, 100), random.uniform(1.0, 100.0)),
        ("Item 10", random.randint(1, 100), random.uniform(1.0, 100.0))
    ]

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)', items)
    conn.commit()
    conn.close()

init_db()
populate_inventory()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute(query, args)
    result = cursor.fetchall()
    conn.close()
    return (result[0] if result else None) if one else result

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check username and password against the database (you'd hash passwords in a real app)
        # For simplicity, let's assume username is 'admin' and password is 'password'
        if username == 'admin' and password == 'password':
            return redirect(url_for('store'))
    return render_template('login.html')

@app.route('/store')
def store():
    query = 'SELECT * FROM inventory'
    items = query_db(query)
    return render_template('store.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
