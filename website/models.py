from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import UserMixin
import datetime

mail = Mail()

db = SQLAlchemy()

#our model


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(210))
    first_name = db.Column(db.String(150))
    phone = db.Column(db.String(10))
    active = db.Column(db.Boolean(), default= False)
    api_id = db.relationship('Algo',uselist = False, backref='api')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True,nullable = False)
    details = db.Column(db.String(100), nullable = True)
    role = db.relationship('User', backref='role')  #back ref should be database name in small


# Define icici api model
class Algo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(150), unique=True)
    converted_key = db.Column(db.String(150), unique=True)
    api_secret = db.Column(db.String(150), unique=True)
    api_sesion = db.Column(db.String(50), unique=False, nullable = True)
    session_time = db.Column(db.String(50), unique=False, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

# Option Expiry Dates
class Optionexpire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.Date, nullable =False)

class Equity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(10))
    shortname = db.Column(db.String(30))
    company_name = db.Column(db.String(50))
    isin = db.Column(db.String(15))
    exchange_name = db.Column(db.String(30))

class Indices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50))
    shortname = db.Column(db.String(50))
    company_name = db.Column(db.String(50))
    isin = db.Column(db.String(15))
    exchange_name = db.Column(db.String(30))

class Sgb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50))
    shortname = db.Column(db.String(50))
    company_name = db.Column(db.String(50))
    isin = db.Column(db.String(15))
    exchange_name = db.Column(db.String(30))