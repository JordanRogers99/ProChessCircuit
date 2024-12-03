from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Initialize the database (to be run only once for creating the table)
def init_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')

# Route to display and handle login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists
        with sqlite3.connect('users.db') as conn:
            cursor = conn.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):  # Check hashed password
                session['user_id'] = user[0]  # Store the user's ID in session
                session['username'] = user[1]  # Store the username in session
                flash('Login successful!', 'success')
                return redirect(url_for('index'))  # Redirect to home page
            else:
                flash('Invalid username or password', 'danger')

    return render_template('login.html')  # Render login form

# Home page after login
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f"Hello, {session['username']}! Welcome to your homepage."

# Run the app
if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)