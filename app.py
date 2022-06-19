from App import app
from flask_socketio import SocketIO, send

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handle_message(message):
    print("Received messsage: " + message)
    if message != "User connected":
        send(message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5000)
