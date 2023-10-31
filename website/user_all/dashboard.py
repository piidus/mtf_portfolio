try:
    from flask import Blueprint, render_template, flash, current_app, request, redirect, url_for, jsonify, make_response
    from flask_login import login_user, login_required, logout_user, current_user
    from website.strategy import SessionKeyGenerator
    from website.models import db, User, Algo
    import urllib, datetime, pytz, time
except Exception as e:
    print('Error in user_all/dashboard.py', e)

all_user = Blueprint('all_user', __name__)

@all_user.route('/dashboard', methods = ['POST', 'GET'])
def dashboard():
    return render_template('user/all_user.html', user = current_user)

@all_user.route('/check_url')
def check_api_login_url():
    target_url = 'https://127.0.0.1/?apisession='
    max_wait_time = 5  # Maximum time to wait (in seconds)
    polling_interval = 1  # Interval for checking the URL (in seconds)
    start_time = time.time()

    # while time.time() - start_time <= max_wait_time:
    #     # Perform a check on the target_url, and if it meets the condition you require, break the loop
    #     # You might want to use libraries like requests to perform URL requests here.
    #     # Example:
    #     import requests
    #     response = requests.get(target_url)
    #     response.s
    #     if some_condition_met(response):
    #         break
    #     time.sleep(polling_interval)
    data = {'sns': 'I lave tou'}
    return jsonify(data)

@all_user.route('/icici_login', methods = ['POST'])
def icici_login():
    
    # if request.method == 'POST' : # and data['param'] == 'login_api':
    if request.method == 'POST' and request.get_json().get('param') == 'login_api':  # Your code here
        try:
            data = request.get_json()
        except Exception as e:
            print(e)
        # print(data)
    
        user_id = data['user_id']
        api = Algo.query.filter_by(user_id = user_id).first()
        api_key=api.converted_key        
        try:
            
            login_url = "https://api.icicidirect.com/apiuser/login?api_key="+(api_key)
            print(login_url)
            response = {'new_link': login_url}
            current_app.logger.info(msg='New tab triggered')
        except Exception as e:
            print('Error in icici login', e)
        return jsonify(response)

@all_user.route('/icici_cred', methods = ['POST','GET']) 
def input_cred():
    # Manual Session Key Input
    if request.method == 'POST' and 'session_key' in request.form:
        algo = Algo.query.filter_by(user_id=current_user.id).first()
        dt = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%h-%dT%H:%M:%S')
        ses = request.form.get('session_key')
        algo.api_sesion= ses
        algo.session_time = dt
        try:
            db.session.commit()
        except Exception as e:
            flash('error in manual input', category='error')
        else:
            flash(message='Manually inster complete', category='success')
    # Credential Input
    if request.method == 'POST' and 'cred_input' in request.form:
        # Check api is already registered on api or not
        algo_check = Algo.query.filter_by(user_id = current_user.id).first()
        if algo_check:
            flash(message='Credential already registered', category='error')
            # print('already Entered')
            current_app.logger.error(f"{current_user.id} : want to insert again cred")
        else:
            user = User.query.filter_by(id = current_user.id).first()
            api_key = request.form.get('api_id')
            decoded_api_key = urllib.parse.quote_plus(api_key)
            api_sec = request.form.get('api_sec')
            
            # print(api_key, api_sec, username, password)
            try:
                algo = Algo(api_key = api_key, converted_key = decoded_api_key, api_secret = api_sec,  user_id = current_user.id)
                db.session.add(algo)
                db.session.commit()
                current_app.logger.info(f"{current_user.id} : insert new cred")
            except Exception as e:
                print(e)
                db.session.rollback()
                flash('Error in api', category='error')
                current_app.logger.error(f"{current_user.id} : Have some issue")
            else:
                flash('Api Entry Sucessfull', category='success')


    try:
        
        algo = Algo.query.filter_by(user_id=current_user.id).first()
        login_url = "https://api.icicidirect.com/apiuser/login?api_key="+(algo.converted_key)
        login_time = str(algo.session_time).split('T')
    
        data = {'algo_time':f"{login_time[0]} Time : {login_time[1]}",
                'login_link' : login_url}
    except:
        data={'algo_time':'Please put you api first'}
    return render_template('user/icici_login.html', user = current_user, data = data)