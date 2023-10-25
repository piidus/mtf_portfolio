from flask import Flask, render_template, flash, request, redirect, url_for
from .models import db, mail
from flask_login import LoginManager
from .models import User
# from flask_mail import Mail



def create_app():
    #create the object of Flask
    app  = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    mail.init_app(app)
    


    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    

    # from .models import User, Note
    
    with app.app_context():
        db.create_all()

    
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
