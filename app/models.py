from app import db
from datetime import datetime

# Stores user information
class User(db.Model):
    id = db.Column(db.INTEGER, primary_key = True)
    username = db.Column(db.TEXT, nullable = False, unique=True)
    password = db.Column(db.TEXT, nullable = False)

    # Define the relationship with the Message model
    sent_messages = db.relationship('Message', back_populates='sender')
    user_chats = db.relationship('UserChat', back_populates='user')

# Stores message content
class Message(db.Model):
    msg_id = db.Column(db.Integer, primary_key = True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False)
    msg_text = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False)

    # Relationship between Message and User model
    sender = db.relationship('User', back_populates = 'sent_messages', foreign_keys = [sender_id])

# Stores chat details 
class Chats(db.Model):
    chat_id = db.Column(db.Integer, primary_key = True)
    chat_name = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.TIMESTAMP, nullable = False)

    # Relationship between Chats and UserChat model
    user_chats = db.relationship('UserChat', back_populates = 'chat')

# Bridging model to connect chats with users
class UserChat(db.Model):
    user_chat_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id', ondelete = 'CASCADE'), nullable = False)

    # Relationship between UserChat and User model
    user = db.relationship('User', back_populates = 'user_chats')
    # Relationship between UserChat and Chats model
    chat = db.relationship('Chats', back_populates = 'user_chats')
