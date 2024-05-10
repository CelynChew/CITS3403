from app import db
from datetime import datetime
from flask_login import UserMixin

# Stores user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    # Relationship with the Message model
    sent_messages = db.relationship('Message', back_populates='sender', foreign_keys='Message.sender_id')
    user_chats = db.relationship('UserChat', back_populates='user')
    # Relationship with the Chats model
    created_chats = db.relationship('Chats', back_populates='creator')

    def __repr__(self):
        return f"User('{self.username}')"

    def get_id(self):
        return str(self.id)

# Stores message content
class Message(db.Model):
    msg_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_sender_id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_receiver_id', ondelete='CASCADE'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id', ondelete='CASCADE'), nullable=False)
    msg_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    # Relationship between Message and User model
    sender = db.relationship('User', back_populates='sent_messages', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    # Relationship between Message and Chats model
    chat = db.relationship('Chats', backref='messages')

# Stores chat details 
class Chats(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    chat_name = db.Column(db.VARCHAR(100), nullable=False)
    receiver_chat_name = db.Column(db.VARCHAR(100), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))  

    # Relationship between Chats and UserChat model
    user_chats = db.relationship('UserChat', back_populates='chat', cascade='all, delete')
    # Relationship with the User model
    creator = db.relationship('User', back_populates='created_chats')

# Bridging model to connect chats with users
class UserChat(db.Model):
    user_chat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id', ondelete='CASCADE'), nullable=False)

    # Relationship between UserChat and User model
    user = db.relationship('User', back_populates='user_chats')
    # Relationship between UserChat and Chats model
    chat = db.relationship('Chats', back_populates='user_chats')
