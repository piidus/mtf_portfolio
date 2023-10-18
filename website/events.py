from flask_socketio import SocketIO
from flask_socketio import emit
import random, time
socketio = SocketIO()
@socketio.on('connect')
def socket_connect():
    print('Client Connected')



def generate_random_numbers():
    total =2
    while total>0:
        time.sleep(1)  # Adjust this delay based on your needs
        num = random.randint(1, 1000)
        # print(num)
        if num % 2 ==0:
            emit('even_num', num)
        if num % 17 == 0:
            print(num)
            emit('random_number', num)
            total-=1

@socketio.on('message')
def handle_message(message):
    print(message)
    emit('response', message+'hello')  # Example WebSocket event handler
    # generate_random_numbers()