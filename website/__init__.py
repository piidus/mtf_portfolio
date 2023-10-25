from flask import Flask, render_template, flash, request, redirect, url_for
from .models import db
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail



def create_app():
    #create the object of Flask
    app  = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    mail = Mail(app)
    


    from .views import views

    app.register_blueprint(views, url_prefix='/')
    

    # from .models import User, Note
    
    with app.app_context():
        db.create_all()

    return app
