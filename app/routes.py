from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Message, Chats, UserChat
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
    if 'username' not in session:
        return render_template('login.html', alert_message="Opps.. You need to log in before accessing the chatroom.") # Redirect user if not authenticated
    
    # Get the username from the session
    username = session['username']
    
    # Retrieve chats for logged in user
    conn = get_db_connection()
    userchats = conn.execute('''
        SELECT c.chat_id, c.chat_name
        FROM chats c
        INNER JOIN user_chats uc ON c.chat_id = uc.chat_id
        INNER JOIN users u ON uc.user_id = u.id
        WHERE u.username = ?
    ''', (username,)).fetchall()
    conn.close()
    
    return render_template('chatroom.html', user_chats=userchats)

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

# Route to handle creating chat
@app.route('/create_chat', methods=['POST'])
def create_chat():
    if request.method == 'POST':
        chat_name = request.json['chat_name']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        conn = get_db_connection()
        try:
            # Insert new chat into the chats table
            cursor = conn.execute('INSERT INTO chats (chat_name, created_at) VALUES (?, ?)', (chat_name, timestamp))
            chat_id = cursor.lastrowid  # Get the ID of the inserted chat
            
            # Get the user ID of the current user
            username = session['username']
            user_id = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()['id']
            
            # Insert into the user_chats table to link the user with the chat
            conn.execute('INSERT INTO user_chats (user_id, chat_id) VALUES (?, ?)', (user_id, chat_id))

            conn.commit()
            conn.close()
            return jsonify({"message": "Chat created successfully"})
        except sqlite3.Error as er:
            conn.close()
            return jsonify({"error": str(er)})


# Route to show chats - GET for displaying chats and DELETE for removing chats
@app.route('/chats', methods=['GET', 'DELETE'])
def show_chats():
    # Check if user is logged in
    if 'username' not in session:
        return render_template('login.html', alert_message="Opps.. You need to log in before accessing the chatroom.") # Redirect user if not authenticated
    
    # Get the username from the session
    username = session['username']
    
    # Connect to the database
    conn = get_db_connection()
    
    # Handling GET request (chat display)
    if request.method == 'GET':
        # Retrieve chats for logged-in user
        user_chats = conn.execute('''
            SELECT c.chat_id, c.chat_name, c.created_at
            FROM chats c
            INNER JOIN user_chats uc ON c.chat_id = uc.chat_id
            INNER JOIN users u ON uc.user_id = u.id
            WHERE u.username = ?
        ''', (username,)).fetchall()
        
        # Close the database connection
        conn.close()
        
        # Create a list to store chat data
        chat_data = []
        for chat in user_chats:
            chat_data.append({
                'chat_id': chat['chat_id'],
                'chat_name': chat['chat_name'],
                'created_at': chat['created_at']
            })
        
        # Return JSON response containing chat information
        return jsonify(chats=chat_data)
    
    # Handling DELETE request (chat removal)
    if request.method == 'DELETE':
        # Get the chat_id to delete
        chat_id = request.json.get('chat_id')

        # Delete the chat from the database
        conn.execute('DELETE FROM user_chats WHERE chat_id = ?', (chat_id,))
        conn.execute('DELETE FROM chats WHERE chat_id = ?', (chat_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Chat deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
