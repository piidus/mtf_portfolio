try:
    from flask import Blueprint, render_template, flash, current_app, request, redirect, url_for, jsonify, make_response, abort
    from flask_login import login_user, login_required, logout_user, current_user
    import urllib, datetime, pytz, time, uuid
    from website.strategy import ShareGeniousStrangle, PivotTrading
    from website.models import db, User, Algo, Optionexpire, Advance_order, Order
    from website.utils import Breeze_api, Icici_Connect

    # from main import app
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

@all_user.route('/icici_login/<string:id>/', methods = ['GET', 'POST'])
def icici_login(id):
    print('It Hitted : --------------------------------;', id)
    apisession = request.args.get('apisession')
    print(apisession)
    if apisession:
        try:
            algo = Algo.query.filter_by(user_id = id).first()
            algo.api_sesion = apisession
            algo.session_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%h-%dT%H:%M:%S')
            db.session.commit()
        except Exception as e:
            print(e)
        last_five_digits = apisession[-8:]
        print(f"Last 5 digits of apisession: {last_five_digits}")
        # Add your custom code here to perform actions based on the last 5 digits
    return "OK"

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
                algo = Algo(api_key = api_key, converted_key = decoded_api_key, api_secret = api_sec,  user_id = user.id)
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
    # Credential del
    if request.method == 'POST' and 'cred_delete' in request.form:
        try:
            api_key = Algo.query.filter_by(user_id = current_user.id).first()
            db.session.delete(api_key)
            db.session.commit()
            flash('api deleted', 'info')
        except Exception as e:
            flash(f"{e}", 'error')

    
    data = {}
    try:
        algo = Algo.query.filter_by(user_id=current_user.id).first()
        # print(algo.converted_key)
        login_url = f"https://api.icicidirect.com/apiuser/login?api_key={algo.api_key}"
        # print(login_url)
        
        data['login_link'] = login_url
    except Exception as e:
        data['algo_time'] = 'Please put you api first'
    else:
        try:
            # algo = Algo.query.filter_by(user_id=current_user.id).first()
            login_time = str(algo.session_time).split('T')
            # print("hello")    
            data['algo_time'] = f"{login_time[0]} Time : {login_time[1]}"
                      
        except:
            data['algo_time'] = 'Please Login'
    # print('a',data)
    return render_template('user/icici_login.html', user = current_user, data = data)

# Check Connection 
@all_user.route('/check_connection', methods = ['GET', 'POST'])
def check_connection():
    algo = Algo.query.filter_by(user_id = current_user.id).first()
    data = {}
    try:
        api = Breeze_api(api_key=algo.api_key, api_secret=algo.api_secret, api_session=algo.api_sesion)
        _, _, icici = Icici_Connect(api_key=algo.api_key, api_session=algo.api_sesion)
        
    except Exception as e:
        print(e)
       
        data['connection'] = 0
        data['date'] = datetime.datetime.now()
        return jsonify(data)
    else:
        data['total_token'] = 1
        data['connection'] = 1
        data['date'] = datetime.datetime.now()
        return jsonify(data)
    
# Strategy Page functionns ***********************

# main strategy page
@login_required
@all_user.route('/dashboard/strategy', methods = ['GET', 'POST'])
def strategy_page():
    if request.method == 'POST' and 'trade'in request.form:
        stock_name = request.form.get('stock_name')
        lot = request.form.get('lot')
        expiry = request.form.get('expiry')
        if expiry:
            try:
                # print('stock_name :', stock_name, "lot", lot, 'expiry : ', expiry)
                uid = f"{current_user.id}-{str(uuid.uuid4().int)}"
                # created = datetime.datetime.now().replace(microsecond=0)
                # Save To Database
                adv = Advance_order(strategy = 'sherowl', symbol = stock_name, u_no = uid, user_id = current_user.id)
                db.session.add(adv)
                db.session.commit()
                try:
                    from main import app
                except Exception as e:
                    print(e)
                strangle = ShareGeniousStrangle(stock_name=stock_name, expiry=expiry, lot=lot, uid = uid, app=app)
                flash(message=('I Check', stock_name, lot, expiry), category='info')
            except Exception as e:
                flash(f'Please contact to Admin :: {e}', category= 'error')
        else:
            flash('Please Check Expiry Dates', 'error')
    # Delete a Order
    # Delete a order
    if request.method == 'POST' and 'order_delete' in request.form:
        try:
            adv_uno = request.form.get('order_id')
            # print(adv_uno)
            row = Advance_order.query.filter_by(u_no = adv_uno).first()
            # print(row)
            row.status = 'stop'
            db.session.commit()
            flash(message='order stopped', category='info')

        except Exception as e:
            flash(message=e, category='error')
        return redirect(url_for('all_user.strategy_page'))

    # Return to page
    current_position = Order.query.filter(Order.exchange_id.isnot(None)).all()
    current_date = datetime.datetime.now().date()
    nifty = Optionexpire.query.filter_by(name = 'NIFTY').filter(Optionexpire.end_date >= current_date).all()    
    nifty_ = sorted([i.end_date.strftime('%Y-%m-%d') for i in nifty])
    bnknifty = Optionexpire.query.filter_by(name = 'CNXBAN').filter(Optionexpire.end_date >= current_date).all()    
    # print(bnknifty)
    bnknifty_ = sorted([i.end_date.strftime('%Y-%m-%d') for i in bnknifty])
    # print(bnknifty_)
    all_order = Advance_order.query.filter_by(user_id = current_user.id, status = 'due').all()[::-1]
    data = {}
    data['expiry'] = {'nifty': nifty_,
                      'bnknifty' : bnknifty_}
    data['orders'] = all_order
    data['positions'] = current_position
    # print(data['positions'])
    # data = json.dumps(data)
    # data = 2
    return render_template('user/strategy.html', user = current_user, data = data)

# Fetch expiry
@all_user.route('/fetch_expiry', methods = ['POST'])
def fetch_expiry():
    current_date = datetime.datetime.now().date()
    nifty = Optionexpire.query.filter_by(name = 'NIFTY').filter(Optionexpire.end_date >= current_date).all()    
    nifty_ = sorted([i.end_date.strftime('%Y-%m-%d') for i in nifty])
    bnknifty = Optionexpire.query.filter_by(name = 'CNXBAN').filter(Optionexpire.end_date >= current_date).all()    
    # print(bnknifty)
    bnknifty_ = sorted([i.end_date.strftime('%Y-%m-%d') for i in bnknifty])
    expiry = {'nifty': nifty_,
            'bnknifty' : bnknifty_}
    return jsonify(expiry)


def user_role(role = ''):
    "It Check user authentication just call the function inside function"
    
    if current_user.role:
        if current_user.role.name in role:
            def func():
                print('ok')
                return func
        else:
            print('not ok')
            abort(code=500)
    else:
        abort(code=500)
    #     def func():
    #         return func
    # else:
    #     abort(500) 

############### NARU ALERT STRATEGY###################
@login_required
@all_user('/')
def fetch_alert():
    pass
######################## pivot Strategy ##########################

@login_required
@all_user.route('/pivot_dashboard',  methods = ['GET', 'POST'])
def pivot_order():
    user_role(['admin'])
    if request.method =='POST' and 'option_trade' in request.form:
        stock_name = request.form.get('ticker')
        expiry_date = request.form.get('expiry')
        # first call history and calculate pivot
        
        pivot = PivotTrading(userid=current_user.id)
        pivot.calculate_pivot(stockname=stock_name)
        flash((stock_name, expiry_date,), 'info')

    # Retun to page
    current_date = datetime.datetime.now().date()
    nifty = Optionexpire.query.filter_by(name = 'NIFTY').filter(Optionexpire.end_date >= current_date).all()    
    nifty_ = sorted([i.end_date.strftime('%Y-%m-%d') for i in nifty])
    bnknifty = Optionexpire.query.filter_by(name = 'CNXBAN').filter(Optionexpire.end_date >= current_date).all()    
    # print(bnknifty)
    bnknifty_ = sorted([i.end_date.strftime('%Y-%m-%d') for i in bnknifty])
    # print(bnknifty_)
    
    data = {}
    data['expiry'] = {'nifty': nifty_,
                      'cnxban' : bnknifty_}
    return render_template('user/pivot_dashboard.html', user =  current_user, data = data)


# get api id and others
@all_user.route('/user_details', methods = ['GET', 'POST'])
def user_details():
    print('it hitted', current_user.id)
    userid = current_user.id
    algo = Algo.query.filter_by(user_id = userid).first()
    # Connect icici connect for id and token
    algo_id, algo_token, algo_session_token = Icici_Connect(api_key=algo.api_key, api_session=algo.api_sesion)
    print(algo_id, algo_token, algo_session_token)
    data = {'algo_user_id': algo_id,
            'algo_token': algo_token,
            'total_token': algo_session_token}
    return jsonify({'ok': 200,
                    'data': data})


