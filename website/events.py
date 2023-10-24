
from .models import socketio
import random,time, datetime
import threading


# @socketio.on('connect')
# def connect():
#     print(f'Client connected:')
#     emit('user_info', 500)

@socketio.on('disconnect', namespace='/my_namespace')
def disconnect():
    print(f'Client disconnected: ')

# @socketio.on('custom_event')
# def custom_event():
#     print(f'Received custom event from js')
    # emit('receive quote')
    # Perform actions upon receiving a custom event
def func_1():
    for _ in range(10):
        time.sleep(5)
        num = random.randint(5,5000)
        message = f'Hello Sudip : {num, datetime.datetime.now()}'
        try:
            t = socketio.emit('custom_event', message)
            print(f'Sent: {message}', t)

        except Exception as e:
            print(e)

@socketio.on('send_date')
def handle_date(data):
    print('data from js', data)
    socketio.emit('custom_event', 'It comes from backend')
    # func_1()
    t = threading.Thread(target=func_1, args=(socketio.emit,))
    t.daemon = True 
    t.start()