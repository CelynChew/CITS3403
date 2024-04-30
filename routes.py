from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a table for users if it doesn't exist
def create_table():
    conn = get_db_connection()
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            username TEXT UNIQUE, 
            password TEXT
        )
        ''')

    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS chats (
            chat_id INTEGER PRIMARY KEY, 
            user_id INTEGER,
            messages TEXT, 
            timestamp DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
        )
        ''')
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
            session['username'] = username
            # User authenticated successfully, redirect to intro page with username
            return redirect(url_for('intro', username=username))
        else:
            # Authentication failed, render login page with error message
            error_message = 'Invalid username or password'
    
    # If it's a GET request, render the login page
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

# Route to serve the introduction page
@app.route('/intro/<username>')
def intro(username):
    return render_template('intro.html', username=username)

# Defining route for using chatroom features
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

# Route to serve the chatroom
@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if not session.get('authenticated'):  # Check if user is authenticated
        return render_template('login.html', alert_message="Opps.. You need to log in before accessing the chatroom.") # Redirect user if not authenticated
    
    if request.method == 'POST':
        username = request.form['username']
        messages = request.form['messages']
        timestamp = datetime.now()

        conn = get_db_connection()
        user = conn.execute('SELECT user_id FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            user_id = user['user_id']
            # Insert messages into the chats table
            conn.execute('INSERT INTO chats (user_id, messages, timestamp) VALUES (?, ?, ?)', (user_id, message, timestamp))
            conn.commit()
        conn.close()   
        return redirect(url_for('chatroom'))
    
    # Handle receiving messages
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM chats').fetchall()
    conn.close()
    
    return render_template('chatroom.html', messages=messages)

# Route to handle senidng the message 
@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        message = request.json['message']
        username = session['username']
        timestamp = datetime.now()

        conn = get_db_connection()
        user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            user_id = user['id']
            # Insert messages into the chats table
            conn.execute('INSERT INTO chats (user_id, messages, timestamp) VALUES (?, ?, ?)', (user_id, message, timestamp))
            conn.commit()
        conn.close()   
        return jsonify({"message": "Message sent successfully"})

# Route to handle retrieving messages
@app.route('/get_messages', methods=['GET'])
def get_messages():
    # Retrieve messages from the database
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM chats').fetchall()
    conn.close()
    messages_list = [{'user_id': message['user_id'], 'message': message['messages'], 'timestamp': message['timestamp']} for message in messages]
    return jsonify(messages_list)

if __name__ == '__main__':
    app.run(debug=True)
