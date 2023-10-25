from flask import Blueprint, render_template, current_app, request
# from .config import db
from .models import db, UserInfo
from flask_mail import Message
import time
import threading



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


