from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a table for users if it doesn't exist
def create_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    conn.close()

create_table()

# Route to handle user login
@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            # User authenticated successfully, redirect to intro page
            return redirect('/intro')
        else:
            # Authentication failed, set error message
            error_message = 'Invalid username or password'
    
    # Render the login page with error message if exists
    return render_template('login.html', error_message=error_message)

# Route to serve the registration page
@app.route('/register', methods=['GET', 'POST']) # GET for displaying registration form, POST for handling registration data.
def registration():
    if request.method == 'POST':
        username = request.form['uName']
        password = request.form['password']
        retype_password = request.form['retypePassword']

        if password != retype_password:
            return render_template('registration.html', error_message='Passwords do not match!')
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect('/')
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('registration.html', error_message='Username already exists! Please choose a different one.')

    return render_template('registration.html')

# Defining route to introduction page
@app.route('/intro')
def intro():
    return render_template('intro.html')

# Defining route to marketplace
@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')

# Defining route to for users to play game
@app.route('/game')
def game():
    return render_template('game.html')

# Defining route for gameplay instructions
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

# Defining route to chatroom
@app.route('/chatroom')
def chatroom():
    return render_template('chatroom.html')

if __name__ == '__main__':
    app.run(debug=True)
