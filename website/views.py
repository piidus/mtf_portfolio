from flask import Blueprint, render_template, request
# from .config import db
from .models import db, UserInfo

views = Blueprint('views', __name__)


#creating our routes
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