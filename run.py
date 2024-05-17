from app import app, db, socketio

# Changing socketio to implement real-time chat app
if __name__ == '__main__':
    socketio.run(app, debug=True)