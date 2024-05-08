from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .models import User, Message, Chats, UserChat
from app import app, db
import os

app.secret_key = os.urandom(24)

# Route to handle user login
@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query database to find the user by username and password
        user = User.query.filter_by(username=username, password=password).first()

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
            return render_template('registration.html', password_error='Passwords do not match!')
        
        # Check if user already exists
        user = User.query.filter_by(username = username).first()
        if user:
            return render_template('registration.html', error_message='Username already exists!')
        
        else:
            user = User(username = username, password = password)
            db.session.add(user)
            db.session.commit()
            # Redirect to a different page after successful registration
            return redirect(url_for('login'))

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
    user_chats = (Chats.query
                  .join(UserChat, Chats.chat_id == UserChat.chat_id)
                  .join(User, UserChat.user_id == User.id)
                  .filter(User.username == username)
                  .all())
    
    return render_template('chatroom.html', user_chats=user_chats)

# Route to handle sending the message 
@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        message = request.json['message']
        username = session['username']
        receiver_username = request.json['chat_name']
        timestamp = datetime.now()

        sender = User.query.filter_by(username = username).first()
        receiver = User.query.filter_by(username = receiver_username).first()
        
        if sender and receiver:
            # Retrieve chat_name from the request
            chat_name = request.json['chat_name']  
            # Query the chat_id based on the chat name
            chat = Chats.query.filter_by(chat_name=chat_name).first()

            if chat:
                chat_id = chat.chat_id

                # Create a new Message object
                new_message = Message(sender_id = sender.id, receiver_id = receiver.id, chat_id = chat_id, msg_text = message, timestamp = timestamp)
                
                # Insert message into the messages table
                db.session.add(new_message)
                db.session.commit()

                return jsonify({"message": "Message sent successfully"})

# Route to display messages
@app.route('/get_messages/<string:chat_name>', methods=['GET'])
def get_messages(chat_name):
    username = session['username']
    user = User.query.filter_by(username = username).first()
    
    # Retrieve chat based on the chat name
    chat = Chats.query.filter_by(chat_name = chat_name).first()

    if chat:
        chat_id = chat.chat_id
        # Check if the logged-in user is a participant in the chat
        participant = UserChat.query.filter_by(user_id=user.id, chat_id=chat_id).first()

        if participant:
            # Retrieve messages from the database for the specified chat
            messages = Message.query.filter_by(chat_id=chat_id).all()

            # Convert the messages to a list of dictionaries
            messages_list = [{'username': message.sender.username, 'receiver_username': message.receiver.username, 'message': message.msg_text, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M')} for message in messages]
            return jsonify(messages_list)
        else:
            return jsonify({"error": "User is not a participant in this chat"})
    else:
        return jsonify({"error": "Chat not found"})

# Route to handle creating chat
@app.route('/create_chat', methods=['POST'])
def create_chat():
    if request.method == 'POST':
        chat_name = request.json['chat_name']
        timestamp = datetime.now()
        
        try:
            # Get the user ID of the current user
            sender_username = session['username']
            
            # Check if the chat already exists
            existing_chat = (Chats.query
                            .join(UserChat, Chats.chat_id == UserChat.chat_id)
                            .join(User, UserChat.user_id == User.id)
                            .filter(User.username == sender_username, Chats.chat_name == chat_name)
                            .first())
            
            if existing_chat:
                return jsonify({"chat_alert": f"Chat with {chat_name} already exists"})


            receiver = User.query.filter_by(username = chat_name).first()
            # Check if the user exists
            if receiver is None:
                return jsonify({"user_alert": f"{chat_name} does not have an account"})
            
            # Insert new chat into the chats table
            chat = Chats(chat_name = chat_name, created_at = timestamp)
            db.session.add(chat)
            db.session.commit()
            
            sender = User.query.filter_by(username = sender_username).first()

            # Insert into the user_chats table to link the user with the chat
            sender_user_chat = UserChat(user_id = sender.id, chat_id = chat.chat_id)
            receiver_user_chat = UserChat(user_id = receiver.id, chat_id = chat.chat_id)

            db.session.add(sender_user_chat)
            db.session.add(receiver_user_chat)
            db.session.commit()

            return jsonify({"message": "Chat created successfully"})
        
        except Exception as err:
            return jsonify({"error": str(err)})

# Route to show chats - GET for displaying chats and DELETE for removing chats
@app.route('/chats', methods=['GET', 'DELETE'])
def show_chats():
    # Check if user is logged in
    if 'username' not in session:
        return render_template('login.html', alert_message="Opps.. You need to log in before accessing the chatroom.") # Redirect user if not authenticated
    
    # Get the username from the session
    username = session['username']
    
    # Handling GET request (chat display)
    if request.method == 'GET':
        # Retrieve chats for logged-in user
        user_chats = (Chats.query
                      .join(UserChat, Chats.chat_id == UserChat.chat_id)
                      .join(User, UserChat.user_id == User.id)
                      .filter(User.username == username)
                      .all())
        
        # Create a list to store chat data
        chat_data = []
        for chat in user_chats:
            chat_data.append({
                'chat_id': chat.chat_id,
                'chat_name': chat.chat_name,
                'created_at': chat.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        # Return JSON response containing chat information
        return jsonify(chats=chat_data)
    
    # Handling DELETE request (chat removal)
    if request.method == 'DELETE':
        # Get the chat_id to delete
        chat_id = request.json.get('chat_id')

        # Delete the chat from the database - Cascade will handle deletion in UserChat
        chat = Chats.query.get(chat_id)
        db.session.delete(chat)
        db.session.commit()

        return jsonify({'message': 'Chat deleted successfully'})

@app.route('/data')
def data():
    # Fetch all users from the database
    users = User.query.all()
    msgs = Message.query.all()
    chats = Chats.query.all()
    user_chats = UserChat.query.all()

    # List to store user data
    user_data = [{
        'id': user.id,
        'username': user.username,
        'password': user.username} for user in users]
    
    msgs_data = [{
        'msg_id': msg.msg_id,
        'sender_id': msg.sender_id,
        'reciever_id':msg.receiver_id,
        'chat_id': msg.chat_id,
        'msg_text': msg.msg_text,
        'timestamp': msg.timestamp} for msg in msgs]
    
    chats_data = [{
        'chat_id': chat.chat_id,
        'chat_name': chat.chat_name,
        'created_at': chat.created_at.strftime("%Y-%m-%d %H:%M:%S")} for chat in chats]
    
    user_chats_data = [{
        'user_chat_id': uchat.user_chat_id,
        'user_id': uchat.user_id,
        'chat_id': uchat.chat_id} for uchat in user_chats]

    return jsonify(users = user_data, msgs = msgs_data, chats = chats_data, user_chats = user_chats_data)

if __name__ == '__main__':
    app.run(debug=True)
