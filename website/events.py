from flask_socketio import SocketIO
from flask_socketio import emit
socketio = SocketIO()
@socketio.on('connect')
def socket_connect():
    print('Client Connected')

@socketio.on('message')
def handle_message(message):
    print(message)
    emit('response', message+'hello')  # Example WebSocket event handler