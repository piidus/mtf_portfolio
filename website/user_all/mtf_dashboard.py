try:
    from flask import Blueprint, current_app, render_template, request, jsonify, session, flash
    from flask_login import current_user, login_required
    import datetime, uuid
    import pandas as pd
    from sqlalchemy import or_, and_
    from website.models import Equity, Tag, Algo, Advance_order, Trigger, db
    from website.utils import Icici_Connect, OhlcPython, OHLCEngine
    # from website.utils.icici_ohlc import OHLCEngine
    from website.strategy import Sharegenious
except Exception as e:
    print('error in userall.mtf_dashboard', e)

mtf_user = Blueprint('mtf_user', __name__)

@login_required
@mtf_user.route('/swing', methods = ['POST', 'GET'])
def swing_home():
    if request.method == 'POST' and 'start_sharegenious' in request.form:
        # mtf csv
        last_adv = Advance_order.query.filter_by(user_id = current_user.id, strategy = 'sharegenious', status = 'due').order_by(Advance_order.id.desc()).first()
        if last_adv:
            flash('order already present', category='error')
        else:
            df = pd.read_csv(filepath_or_buffer='website/static/data/csv/mtf.csv')
            # print(df)
            try:
                from main import app
                uid = f"{current_user.id}-{str(uuid.uuid4().int)}"
                sharegenious = Sharegenious(userid=current_user.id, uid=uid, data=df, app=app).maintain_order_status(status=3)
                if sharegenious == -1:
                    flash('error in connection', category='error')
            except Exception as e:
                print(e)
            flash("order submitted", category='success')
    # Stop Last Order
    if request.method == 'POST' and 'stop_sharegenious' in request.form:
        last_adv = Advance_order.query.filter_by(user_id = current_user.id, strategy = 'sharegenious', status = 'due').order_by(Advance_order.id.desc()).first()
        if last_adv:
            last_adv.status = 'stop'
            db.session.commit()
            # delete the class
            obj = Sharegenious(userid=current_user.id, uid=last_adv.u_no)
            obj.delete_instance()
            print(obj)
            del obj
            flash('Last order Close', category='Info')
        else:
            flash('update need', category='error')

    if request.method == 'POST' and 'sharegenious_action' in request.form:
        action = request.form.get('swing_action')
        uid = request.form.get('u_id')
        print(action, uid)
        if action == 'pause': #maintain order will be pause
            pause_trade = Sharegenious(userid=current_user.id, uid=uid)
            pause_trade.maintain_order_status(status=0)
        elif action == 'stop': #maintain order will be stop
            stop_trade = Sharegenious(userid=current_user.id, uid=uid)
            stop_trade.maintain_order_status(status=-1)
        elif action == 'resume': #maintain order will be stop
            stop_trade = Sharegenious(userid=current_user.id, uid=uid)
            stop_trade.maintain_order_status(status = 1)


    # Returning section
    tags = Tag.query.all()
    adv = Advance_order.query.filter(and_(Advance_order.strategy == 'sharegenious'),or_(Advance_order.status =='due', Advance_order.status == 'pause') )
    
    data = {'tags': tags,
            'adv' : adv}
    return render_template('user/mtf_swing.html', user = current_user, data = data)








@login_required
@mtf_user.route('/mtf', methods = ['POST', 'GET'])
def mtf_home():
    tag_name = ""
    if request.method == 'POST' and 'tagSearch' in request.form:
        tag_name = request.form.get('tags')
    now = datetime.datetime.now().date()
    algo = Algo.query.filter_by(user_id = 2).first()
    print('algo id ::', algo.session_time)
    conn = Icici_Connect(api_key=algo.api_key, api_session=algo.api_sesion)
    # print(conn)
    session['userid'] = conn[0]
    session['token'] = conn[1]
    # ohlc = start_connection(userid=conn[0], token=conn[1])
    
    # print(tag_name)
    # Query equities filtered by the tag name
    try:
        tags = Tag.query.all()
        # for i in tags:
        #     print(i.tagname)
        tags = [i.tagname for i in tags]
        tag_length = len(tags)
        # print(tags)
        equities = Equity.query.join(Equity.tags).filter(Tag.tagname == tag_name).all()
    except Exception as e:
        print(e)
    data = {'equities': equities,
            'conn':conn,
            'tags': tags,
            'taglength': tag_length}
    
    return render_template('user/mtf_dashboard.html', user = current_user, data = data )
@login_required
@mtf_user.route('/mtf_ltp', methods= ['POST'])
def mtf_ltp():
    # ohlc = Ohlc()
    if request.method == 'POST':
        data = request.get_json()
        try:
            token = session['token']
            
            userid = session['userid']
            print(userid, token)
            # c =OhlcPython(userid=userid, session_token=token)
            # OhlcPython(userid=userid, session_token=token) #,stock_list=data['tokenlist'])
            t = OHLCEngine(userid=userid, session_token=token)
            res = t.engine(data['tokenlist'])
            # print(res)
            response = res
            return jsonify(response)
        except Exception as e:
            return jsonify('plese connect it')
        
    

