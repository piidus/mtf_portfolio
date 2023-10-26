from flask import Blueprint, render_template, flash, current_app, request, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from .config import db
from .models import db, User
from flask_mail import Message
import time, random
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
def send_authentication(subject, body, email):
    try:
        msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f" Your Authentication key is :: {body}"

        mail = current_app.extensions['mail']
        mail.send(msg)
    except Exception as e:
        flash(message='Error', category='error')


@auth.route('/', methods = ['GET', 'POST'])
def index():
    
    return render_template('auth/home.html', user = current_user)

# Route to check if an email exists in the list of users.
@auth.route('/check_email', methods=['POST'])
def check_email():

    data = request.get_json()
    email = data['email']
    # print(email)
    suth = random.randint(1000, 90000)
    send_authentication(subject='Authentication Mail', body=suth, email=email)
    user = User.query.filter_by(email=email).first()
    print(user)
    if user:        
        response = {'exists': True}
        
    else:
        response = {'exists': False, 'code':suth}
        # print(data)

    return jsonify(response)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    print(request.form.getlist('signup'))
    if request.method == 'POST':
        email = request.form.get('hiddenEmail')
        # print(email)
        # Check if the input element is 
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone = request.form.get('phone')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(phone)!= 10:
            flash('Please Check the Number', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha1', salt_length=8), phone = phone)
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.index'))

    return render_template("auth/signup.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("auth/login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
