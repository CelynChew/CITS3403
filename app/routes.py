from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from .models import User, Message, Chats, UserChat
from app import app, db
from flask_socketio import send, emit
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from config import Config
from .forms import LoginForm, RegistrationForm, SendMessageForm
import os
from .extensions import socketio

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

## Route to handle user login
@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print("Username:", username)
        print("Password:", password)
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                session['username'] = username
                return redirect(url_for('chatroom', username=username))
            else:
                error_message = 'Invalid password'
        else:
            error_message = 'User not found'
    else:
        print(form.errors)
    return render_template('login.html', error_message=error_message, form=form)

## Route to handle user login
@app.route('/login-m', methods=['GET', 'POST'])
def login_m():
    error_message = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print("Username:", username)
        print("Password:", password)
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                session['username'] = username
                return redirect(url_for('chatroom_m', username=username))
            else:
                error_message = 'Invalid password'
        else:
            error_message = 'User not found'
    else:
        print(form.errors)
    return render_template('login-m.html', error_message=error_message, form=form)

# Route to handle user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)  # Remove the username from the session
    # Remove the session cookie and set it to expire immediately
    response = redirect(url_for('login'))
    response.delete_cookie('session')
    response.set_cookie('session', '', expires=0)
    return response

# Handling 401 errors and redirecting to login page
@app.errorhandler(401)
def unauthorized(error):
    return redirect(url_for('login'))

# Route to serve the registration page
@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        retype_password = form.confirm_password.data

        if password != retype_password:
            return render_template('registration.html', form=form, password_error='Passwords do not match!')

        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('registration.html', form=form, error_message='Username already exists!')

        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            # Redirect to a different page after successful registration
            return redirect(url_for('login'))

    # Render the registration form when the request method is GET
    return render_template('registration.html', form=form)
    
# Route to serve the introduction page
@app.route('/intro/<username>')
@login_required
def intro(username):
    return render_template('intro.html', username=username)

# Defining route for using Tutorial
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')


# Defining route for using Tutorial (Mobile)
@app.route('/tutorial-m')
def tutorial_m():
    return render_template('tutorial-m.html')


# Route to serve the chatroom
@app.route('/chatroom', methods=['GET', 'POST'])
@login_required
def chatroom():
    if 'username' not in session:
        return render_template('login.html', alert_message="Oops.. You need to log in before accessing the chatroom.") # Redirect user if not authenticated

    # Get the username from the session or query parameter
    username = session.get('username') or request.args.get('username')

    form = SendMessageForm()

    if form.validate_on_submit():
        chat_name = form.chat_name.data
        message = form.message.data
        timestamp = datetime.now()
        
        sender_info = User.query.filter_by(username=username).first()
        receiver_info = User.query.filter_by(username=chat_name).first()
        chat = Chats.query.filter_by(chat_name=chat_name).first()
        
        if chat is None:
            chat = Chats.query.filter_by(receiver_chat_name=chat_name).first()

        if chat:
            # Create a new Message object
            new_message = Message(sender_id=sender_info.id, receiver_id=receiver_info.id, chat_id=chat.chat_id, msg_text=message, timestamp=timestamp)

            # Insert message into the messages table
            db.session.add(new_message)
            db.session.commit()
        
    # Retrieve chats for logged in user
    user_chats = (Chats.query
                  .join(UserChat, Chats.chat_id == UserChat.chat_id)
                  .join(User, UserChat.user_id == User.id)
                  .filter(User.username == username)
                  .all())

    # Fetch messages for each chatroom
    chat_messages = {}
    for chat in user_chats:
        messages = Message.query.filter_by(chat_id=chat.chat_id).all()
        chat_messages[chat.chat_name] = messages

    return render_template('chatroom.html', user_chats=user_chats, username=username, chat_messages=chat_messages, form=form)


# Chatroom mobile
@app.route('/chatroom-m')
@login_required
def chatroom_m():
    if 'username' not in session:
        return render_template('login-m.html', alert_message="Oops.. You need to log in before accessing the chatroom.") # Redirect user if not authenticated
    
    # Get the username from the session or query parameter
    username = session.get('username') or request.args.get('username')
    
    # Retrieve chats for logged in user
    user_chats = (Chats.query
                  .join(UserChat, Chats.chat_id == UserChat.chat_id)
                  .join(User, UserChat.user_id == User.id)
                  .filter(User.username == username)
                  .all())
    
    return render_template('chatroom-m.html', user_chats=user_chats, username=username)

# Route to recieve file uploaded by users
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')

# Check if the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    # Create file if it does not exist
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    chat_name = request.form['chat_name']  # Get the chat name from the request
    username = session['username']
    timestamp = datetime.now()

    sender_info = User.query.filter_by(username=username).first()
    receiver_info = User.query.filter_by(username=chat_name).first()

    # Retrieve chats for logged-in user
    user_chats = (Chats.query
                      .join(UserChat, Chats.chat_id == UserChat.chat_id)
                      .join(User, UserChat.user_id == User.id)
                      .filter(User.username == username)
                      .all())
    
    chat = next((chat for chat in user_chats if chat.chat_name == chat_name), None)

    if chat == None:
        chat = next((chat for chat in user_chats if chat.receiver_chat_name == chat_name), None)

    if file and chat:
        # Read the content of the file
        file_content = file.read()
        print("Chat Name:", chat_name)  # Print the chat name
        print(file_content)
        
        # Reset file handle position to the beginning of the file
        file.seek(0)

        # Save the file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], (file.filename))
        with open(file_path, 'wb') as f:
            f.write(file.read())

        new_message = Message(sender_id=sender_info.id, receiver_id=receiver_info.id, chat_id=chat.chat_id, file_name=file.filename, timestamp=timestamp)
        
        db.session.add(new_message)
        db.session.commit()
       
        return jsonify({"message": "Message sent successfully"})
    else:
        return 'No file uploaded'

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Checking the socketio connetion 
@socketio.on("connect")
def handle_connect():
    print("Client connected!")

# Sending the message in real-time using flask-socketio
@socketio.on('message')
def handle_message(data):
    chatroom = session.get('chatroom')
    
    if isinstance(data, dict):
        message = data.get('msg')
        username = session['username']
        chat_name = data.get('chatName')
        timestamp = datetime.now()
        formatted_message = f"{username}: {message} ({timestamp.strftime('%Y-%m-%d %H:%M')})"
        
        print("Received message data:", data)
        
        sender_info = User.query.filter_by(username=username).first()
        receiver_info = User.query.filter_by(username=chat_name).first()
        chat = Chats.query.filter_by(chat_name=chat_name).first()
        
        print(chat)
        
        if chat is None:
            chat = Chats.query.filter_by(receiver_chat_name=chat_name).first()
                
        if chat:
            # Create a new Message object
            new_message = Message(sender_id=sender_info.id, receiver_id=receiver_info.id, chat_id=chat.chat_id, msg_text=message, timestamp=timestamp)
                    
            # Insert message into the messages table
            db.session.add(new_message)
            db.session.commit()

            # Emit the message to all clients in the chat room
            socketio.emit('message', {'msg': formatted_message, 'username': username, 'time_stamp': timestamp.isoformat()}, room=chatroom)

# # Route to handle sending the message 
# @app.route('/send_message', methods=['POST'])
# @login_required
# def send_message():
#     if request.method == 'POST':
#         message = request.json['message']
#         username = session['username']
#         chat_name = request.json['chat_name']
#         timestamp = datetime.now()

#         sender_info = User.query.filter_by(username=username).first()
#         receiver_info = User.query.filter_by(username=chat_name).first()
        
#         # Retrieve chats for logged-in user
#         user_chats = (Chats.query
#                       .join(UserChat, Chats.chat_id == UserChat.chat_id)
#                       .join(User, UserChat.user_id == User.id)
#                       .filter(User.username == username)
#                       .all())
#         print(user_chats)

#         chat = next((chat for chat in user_chats if chat.chat_name == chat_name), None)

#         if chat == None:
#             chat = next((chat for chat in user_chats if chat.receiver_chat_name == chat_name), None)
#         print(chat)

#         if chat:
#             # Create a new Message object
#             new_message = Message(sender_id=sender_info.id, receiver_id=receiver_info.id, chat_id=chat.chat_id, msg_text=message, timestamp=timestamp)
                    
#             # Insert message into the messages table
#             db.session.add(new_message)
#             db.session.commit()

#             return jsonify({"message": "Message sent successfully"})
#         else:
#             return jsonify({"error": "Chat not found"}), 404
                
# Route to retrieve chatId based on chatName
@app.route('/get_chat_id/<chatName>')
@login_required
def get_chat_id(chatName):
    if 'username' in session:  # Check if user is logged in
        logged_in_username = session['username']
        print("Chat name:", chatName)

        # Retrieve the logged-in user from the database
        logged_in_user = User.query.filter_by(username=logged_in_username).first()

        if logged_in_user:
            # Retrieve chats for the logged-in user
            user_chats = (Chats.query
                          .join(UserChat, Chats.chat_id == UserChat.chat_id)
                          .join(User, UserChat.user_id == User.id)
                          .filter(User.id == logged_in_user.id)
                          .all())

            # Find the chat based on whether the logged-in user is the creator or receiver
            for chat in user_chats:
                if chat.chat_name == chatName or chat.receiver_chat_name == chatName:  # Check if the chat name matches
                    if chat.created_by == logged_in_user.id or chat.receiver_chat_name == chatName:  # Check if the logged-in user is the creator
                        print("Chat id:", chat.chat_id)
                        return jsonify({"chatId": chat.chat_id})
                    else:
                        return jsonify({"error": "User is not the creator of the chat"}), 403

            # If the loop completes without finding the chat
            print("Chat not found")
            return jsonify({"error": "Chat not found"}), 404
        else:
            print("User not found")
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "User not logged in"}), 401
    
# Route to display messages
@app.route('/get_messages/<int:chat_id>', methods=['GET'])
@login_required
def get_messages(chat_id):
    username = session['username']
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
            messages_list = []
            for message in messages:
                message_data = {
                    'chat_id': chat_id, 
                    'sender_username': message.sender.username, 
                    'receiver_username': message.receiver.username, 
                    'message': message.msg_text, 
                    'file_name': message.file_name,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M')
                }

                messages_list.append(message_data)

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
        'file_name': msg.file_name,
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
    socketio.run(debug=True)
