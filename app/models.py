from app import db
from datetime import datetime

# Stores user information
class User(db.Model):
    id = db.Column(db.INTEGER, primary_key = True)
    username = db.Column(db.TEXT, nullable = False, unique=True)
    password = db.Column(db.TEXT, nullable = False)

    # Relationship with the Message model
    sent_messages = db.relationship('Message', back_populates='sender', foreign_keys='Message.sender_id')
    user_chats = db.relationship('UserChat', back_populates='user')
    # Relationship with the Chats model
    created_chats = db.relationship('Chats', back_populates='creator')

# Stores message content
class Message(db.Model):
    msg_id = db.Column(db.Integer, primary_key = True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_sender_id', ondelete = 'CASCADE'), nullable = False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_receiver_id', ondelete = 'CASCADE'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id', ondelete='CASCADE'), nullable=False)
    msg_text = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False)
    is_group_message = db.Column(db.Boolean, default=False)  # Flag to indicate if it's a message sent to a group 

    # Relationship between Message and User model
    sender = db.relationship('User', back_populates = 'sent_messages', foreign_keys = [sender_id])
    receiver = db.relationship('User', foreign_keys = [receiver_id])
    # Relationship between Message and Chats model
    chat = db.relationship('Chats', backref='messages')

# Stores chat details 
class Chats(db.Model):
    chat_id = db.Column(db.Integer, primary_key = True)
    chat_name = db.Column(db.VARCHAR(100), nullable = False)
    receiver_chat_name = db.Column(db.VARCHAR(100), nullable = False)
    created_at = db.Column(db.TIMESTAMP, nullable = False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_group_chat = db.Column(db.Boolean, default=False)  # Flag to indicate if it's a group chat

    # Relationship between Chats and UserChat model
    user_chats = db.relationship('UserChat', back_populates = 'chat', cascade = 'all, delete')
    # Relationship with the User model
    creator = db.relationship('User', back_populates = 'created_chats')
    # Relationship with GroupChat model
    group = db.relationship('GroupChat', back_populates='chat')

# Bridging model to connect chats with users
class UserChat(db.Model):
    user_chat_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id', ondelete = 'CASCADE'), nullable = False)

    # Relationship between UserChat and User model
    user = db.relationship('User', back_populates = 'user_chats')
    # Relationship between UserChat and Chats model
    chat = db.relationship('Chats', back_populates = 'user_chats')

# Model to store group chat details
class GroupChat(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id', ondelete = 'CASCADE'), nullable=False)
    group_name = db.Column(db.VARCHAR(100))
    
    # Relationship between GroupChat and Chats
    chat = db.relationship('Chats', back_populates='group')