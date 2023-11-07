try:
    from flask import Blueprint, current_app, render_template
    from flask_login import current_user, login_required
except Exception as e:
    print('error in userall.mtf_dashboard', e)

mtf_user = Blueprint('mtf_user', __name__)
@login_required
@mtf_user.route('/mtf', methods = ['POST', 'GET'])
def mtf_home():
    data = {}
    return render_template('user/mtf_dashboard.html', user = current_user, data = data)