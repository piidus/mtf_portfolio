try:
    from flask import Blueprint, render_template, flash, current_app, request, redirect, url_for, jsonify, make_response
    from flask_login import login_user, login_required, logout_user, current_user
    from website.strategy import SessionKeyGenerator
    from website.models import db, User
except Exception as e:
    print('Error in user_all/dashboard.py', e)

all_user = Blueprint('all_user', __name__)

@all_user.route('/dashboard', methods = ['POST', 'GET'])
def dashboard():
    return render_template('user/all_user.html', user = current_user)
@all_user.route("/new_tab")
def new_tab():
    response = make_response()
    response.headers["X-My-Header"] = "My Header Value"

    response.headers["Content-Type"] = "text/html"
    response.set_cookie("new_tab", "true")
    response.set_data("<script>window.open('https://www.google.com', '_blank');</script>")

    return response


@all_user.route('/icici_login', methods = ['GET', 'POST'])
def icici_login():
    if request.method == 'POST' and 'api_login' in request.form:
        api_key='i8582*146#NX60853w32X3*56nd8x8l0'
        api_secrect='390N93eS546783t49!586174u63cMv54'
        # login_url = f"https://api.icicidirect.com/apiuser/login?api_key=i8582*146#NX60853w32X3*56nd8x8l0"
        try:
            import urllib   
            login_url = "https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(api_key)
            response = make_response()
            response.headers["X-My-Header"] = api_secrect

            response.headers["Content-Type"] = "text/html"
            response.set_cookie("new_tab", "true")
            response.set_data(f"<script>window.open('{login_url}', '_blank');</script>")
            # session_key = SessionKeyGenerator(api_key, api_secrect,1,1).icici_login()
            # print(session_key)
        except Exception as e:
            print('Error in icici login', e)
        return response




    try:
        # login_time = Algo.query.filter_by(user_id=current_user.id).first()
        login_time = str(login_time.session_time).split('T')
    
        data = {'algo_time':f"{login_time[0]} Time : {login_time[1]}"}
    except:
        data={'algo_time':'Please put you api first'}
    return render_template('user/icici_login.html', user = current_user, data = data)