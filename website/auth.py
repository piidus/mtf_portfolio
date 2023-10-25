from flask import Blueprint, render_template, current_app, request
from flask_login import login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from .config import db
from .models import db, User
from flask_mail import Message
import time
import threading, os



auth = Blueprint('auth', __name__)


#creating our routes

@auth.route('/send_email')
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


@auth.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST' and 'pwd' in request.form:
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        print(user, pwd)
        data = User(username=user, password=pwd)
        db.session.add(data)
        db.session.commit()
    users = User.query.all()
    mail_pwd = "0" #os.environ.get('MAIL_PWD')
    data = {'user': users, 'mail': mail_pwd}

    return render_template('auth/home.html', user = current_user, data= data)


