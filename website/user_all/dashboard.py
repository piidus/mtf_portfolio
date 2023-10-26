try:
    from flask import Blueprint, render_template, flash, current_app, request, redirect, url_for, jsonify
    from flask_login import login_user, login_required, logout_user, current_user
    from website.strategy import SessionKeyGenerator
    from website.models import db, User
except Exception as e:
    print('Error in user_all/dashboard.py', e)

all_user = Blueprint('all_user', __name__)

@all_user.route('/dashboard', methods = ['POST', 'GET'])
def dashboard():
    return render_template('user/all_user.html', user = current_user)

@all_user.route('/icici_login', methods = ['GET', 'POST'])
def icici_login():
    if request.method == 'POST' and 'api_login' in request.form:
        try:    
            session_key = SessionKeyGenerator(1,1,1).login()
        except Exception as e:
            print('Error in icici login', e)




    try:
        # login_time = Algo.query.filter_by(user_id=current_user.id).first()
        login_time = str(login_time.session_time).split('T')
    
        data = {'algo_time':f"{login_time[0]} Time : {login_time[1]}"}
    except:
        data={'algo_time':'Please put you api first'}
    return render_template('user/icici_login.html', user = current_user, data = data)