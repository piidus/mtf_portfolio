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
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable = True)
    

# # Define the Role data-model
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), unique=False)
#     details = db.Column(db.String(100), nullable = True)
#     role = db.relationship('User', backref='role')  #back ref should be database name in small
    