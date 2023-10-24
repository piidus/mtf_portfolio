from flask import Blueprint, render_template, current_app, request
# from .config import db
from .models import db, UserInfo
from flask_mail import Message
import time
import threading
from .models import socketio


views = Blueprint('views', __name__)


#creating our routes

@views.route('/send_email')
def send_email():
    try:
        recipient = 'sudiipkumarbasu@gmail.com'
        subject = 'This is Testing'
        body = "Hi: This message for email verification"

        msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=[recipient])
        msg.body = body

        mail = current_app.extensions['mail']
        mail.send(msg)

        return "Email sent successfully!"
    except Exception as e:
        return f"Error : {e}"


@views.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST' and 'pwd' in request.form:
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        print(user, pwd)
        data = UserInfo(username=user, password=pwd)
        db.session.add(data)
        db.session.commit()
    users = UserInfo.query.all()
    data = {'user': users}

    return render_template('index.html', data= data)

def check1(app, socket):
    time.sleep(3)
    try:    
        message = "Hello, this is a message from the server!"
        try:
            with app.app_context():
                try:
                    socket.emit('server_event',{'data': 'Hello from the server!'})
                    print('it works')
                except Exception as e:
                    print('inner',e)
        except Exception as e:
            print('first Error', e)
    except Exception as e:
        print('------------------e :',e)

@views.route('/check_status')
def check_status():
    
    try:
        # threading.Timer(interval=3, function= check1, args=[current_app, socketio]).start()
        t = threading.Thread(target=send_message)
        t.start()

    except Exception as e:
        print(e)
    # check1()

    print('------------------------SIO server started on localhost:3000')
    return render_template('check_status.html')


def send_message():
    time.sleep(5)  # Simulate some background task
    print('it trigeered')
    try:
        socketio.emit('server_event', {'data': 'Hello from the server!'}, namespace='/my_namespace')
    except Exception as e:
        print('----',e)


@socketio.on('connect', namespace='/my_namespace')
def test_connect():
    print('socket trigger')
    socketio.emit('server_event', {'data': 'Connected'})
