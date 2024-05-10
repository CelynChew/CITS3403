from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from .models import User, Message, Chats, UserChat
from app import app, db
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from config import Config

app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def before_request():
    session.permanent = False
    app.permanent_session_lifetime = timedelta(minutes=5)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            login_user(user)
            # User authenticated successfully, redirect to intro page with username
            return redirect(url_for('chatroom', username=username))
        else:
            # Authentication failed, render login page with error message
            error_message = 'Invalid username or password'
    
    # If it's a GET request, render the login page
    return render_template('login.html', error_message=error_message)

# Route to handle user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Clear the session
    # Remove the session cookie and set it to expire immediately
    response = redirect(url_for('login'))
    response.delete_cookie('session')
    response.set_cookie('session', '', expires=0)
    return response

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
@login_required
def intro(username):
    return render_template('intro.html', username=username)

# Defining route for using chatroom features
@app.route('/tutorial')
@login_required
def tutorial():
    return render_template('tutorial.html')

# Route to serve the chatroom
@app.route('/chatroom', methods=['GET', 'POST'])
@login_required
def chatroom():
    # If the username parameter is missing from the URL, redirect with the username
    if session.get('logged_in'):
        username = session['username']
    if 'username' not in request.args:
        return redirect(url_for('chatroom', username=current_user.username))
    
    # Get the username from the query parameters
    username = request.args.get('username')

    # Ensure that the logged-in user matches the username in the URL
    if current_user.username == username:
        # Retrieve chats for logged-in user
        user_chats = (Chats.query
                      .join(UserChat, Chats.chat_id == UserChat.chat_id)
                      .join(User, UserChat.user_id == User.id)
                      .filter(User.username == username)
                      .all())
        
        return render_template('chatroom.html', user_chats=user_chats, username=username)
    else:
        # If the username in the URL doesn't match the logged-in user, redirect to the login page
        return redirect(url_for('login'))
    
# Route to handle sending the message 
@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    if request.method == 'POST':
        message = request.json['message']
        username = current_user.username
        chat_name = request.json['chat_name']
        timestamp = datetime.now()

        sender_info = User.query.filter_by(username=username).first()
        receiver_info = User.query.filter_by(username=chat_name).first()
        
        chat = Chats.query.filter_by(chat_name=chat_name).first()

        if chat == None:
            chat = Chats.query.filter_by(receiver_chat_name=chat_name).first()
        
        print(chat)
        
        if chat:
            # Create a new Message object
            new_message = Message(sender_id=sender_info.id, receiver_id=receiver_info.id, chat_id=chat.chat_id, msg_text=message, timestamp=timestamp)
                    
            # Insert message into the messages table
            db.session.add(new_message)
            db.session.commit()

            return jsonify({"message": "Message sent successfully"})
        else:
            return jsonify({"error": "Chat not found"})
        
# Route to retrieve chatId based on chatName
@app.route('/get_chat_id/<chatName>')
@login_required
def get_chat_id(chatName):
    logged_in_username = current_user.username
    
    # Query the database to find the user who created the chat
    creator = User.query.join(Chats, User.id == Chats.created_by).filter(Chats.chat_name == chatName).first()
    
    # Find the chat based on whether the logged-in user is the creator
    chat = None
    if creator and creator.username == logged_in_username:  # Check if creator is not None and if the logged-in user is the creator
        chat = Chats.query.filter_by(chat_name=chatName).first()
    else:  # If the logged-in user is the receiver
        chat = Chats.query.filter_by(receiver_chat_name=chatName).first()
    
    if chat:
        print("Chat found:", chat)
        return jsonify({"chatId": chat.chat_id})
    else:
        print("Chat not found")
        return jsonify({"error": "Chat not found"}), 404

# Route to display messages
@app.route('/get_messages/<int:chat_id>', methods=['GET'])
@login_required
def get_messages(chat_id):
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    
    # Retrieve chat based on the chat id
    chat = Chats.query.get(chat_id)

    if chat:
        # Check if the logged-in user is a participant in the chat
        participant = UserChat.query.filter_by(user_id=user.id, chat_id=chat_id).first()

        if participant:
            # Retrieve messages from the database for the specified chat
            messages = Message.query.filter_by(chat_id=chat_id).all()

            # Convert the messages to a list of dictionaries
            messages_list = [{'chat_id': chat_id, 
                              'sender_username': message.sender.username, 
                              'receiver_username': message.receiver.username, 
                              'message': message.msg_text, 
                              'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M')} 
                             for message in messages]
            return jsonify(messages_list)
        else:
            return jsonify({"error": "User is not a participant in this chat"})
    else:
        return jsonify({"error": "Chat not found"})

# Route to handle creating chat
@app.route('/create_chat', methods=['POST'])
@login_required
def create_chat():
    if request.method == 'POST':
        chat_name = request.json['chat_name']
        timestamp = datetime.now()
        
        try:
            # Get the user ID of the current user
            sender_username = current_user.username

             # User who is creating the chat
            created_by = User.query.filter_by(username = sender_username).first()
            
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
            chat = Chats(chat_name = chat_name, created_at = timestamp, created_by = created_by.id, receiver_chat_name = sender_username)
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
@login_required
def show_chats():
    # Get the username from the session
    username = current_user.username

    # Get logged in user information
    logged_in = User.query.filter_by(username=username).first()

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
            # Determine the chat name based logged in account
            if chat.created_by == logged_in.id:
                chat_name = chat.chat_name
            else:
                chat_name = chat.receiver_chat_name

            chat_data.append({
                'chat_id': chat.chat_id,
                'chat_name': chat_name,
                'created_at': chat.created_at.strftime('%Y-%m-%d %H:%M')
            })

        # Return JSON response containing chat information
        return jsonify(chats=chat_data)

    # Handling DELETE request (chat removal)
    if request.method == 'DELETE':
        # Get the chat_id to delete
        chat_id = request.json.get('chat_id')

        # Delete associated messages first
        Message.query.filter_by(chat_id=chat_id).delete()

        # Delete the chat from the database - Cascade will handle deletion in UserChat
        chat = Chats.query.get(chat_id)
        db.session.delete(chat)
        db.session.commit()

        return jsonify({'message': 'Chat deleted successfully'})


@app.route('/data')
@login_required
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
        'creator_chat_name': chat.chat_name,
        'created_at': chat.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        'receiver_chat_name': chat.receiver_chat_name,
        'created_by': chat.created_by} for chat in chats]
    
    user_chats_data = [{
        'user_chat_id': uchat.user_chat_id,
        'user_id': uchat.user_id,
        'chat_id': uchat.chat_id} for uchat in user_chats]

    return jsonify(users = user_data, msgs = msgs_data, chats = chats_data, user_chats = user_chats_data)

if __name__ == '__main__':
    app.run(debug=True)
