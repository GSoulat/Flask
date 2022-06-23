from App import app
# from flask_socketio import SocketIO, send
import os

# socketio = SocketIO(app, cors_allowed_origins='*')

# @socketio.on('message')
# def handle_message(message):
#     print("Received messsage: " + message)
#     if message != "User connected":
#         send(message, broadcast=True)



if __name__ == '__main__':
    # os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_ENV'] = 'production'
    app.run(host='0.0.0.0',port=5000)
