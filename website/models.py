from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, func, Integer, String
from flask_mail import Mail
from flask_login import UserMixin
import datetime

mail = Mail()

db = SQLAlchemy()

#our model


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    password = Column(String(210))
    first_name = Column(String(150))
    phone = Column(String(10))
    active = Column(db.Boolean(), default= False)
    api_id = db.relationship('Algo',uselist = False, backref='api')
    role_id = Column(Integer, db.ForeignKey('roles.id'))
    advance_order_id = db.relationship('Advance_order', backref = 'advance_order' )

# Advance order
class Advance_order(db.Model):
    __table_name__ = 'advance_order'
    id = Column(Integer, primary_key=True)
    strategy = Column(String(30), nullable = False)
    symbol = Column(String(10))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    u_no = Column(String(50), unique = True)
    status = Column(String(20), default='due')
    percentage = Column(String(10), nullable=True)
    cover = Column(String(10), nullable=True)
    near = Column(String(10), nullable = True)
    extra_1 = Column(String(50), nullable = True)
    extra_2 = Column(String(50), nullable = True)
    extra_3 = Column(String(50), nullable = True)
    user_id = Column(Integer, db.ForeignKey('user.id'))

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True,nullable = False)
    details = Column(String(100), nullable = True)
    role = db.relationship('User', backref='role')  #back ref should be database name in small


# Define icici api model
class Algo(db.Model):
    id = Column(Integer, primary_key=True)
    api_key = Column(String(150), unique=True)
    converted_key = Column(String(150), unique=True)
    api_secret = Column(String(150), unique=True)
    api_sesion = Column(String(50), unique=False, nullable = True)
    session_time = Column(String(50), unique=False, nullable = True)
    user_id = Column(Integer, db.ForeignKey('user.id')) 

# Option Expiry Dates
class Optionexpire(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    end_date = Column(db.Date, nullable =False)

class Indices(db.Model):
    id = Column(Integer, primary_key=True)
    token = Column(String(50))
    shortname = Column(String(50))
    company_name = Column(String(50))
    isin = Column(String(50))
    exchange_name = Column(String(30))

class Sgb(db.Model):
    id = Column(Integer, primary_key=True)
    token = Column(String(50))
    shortname = Column(String(50))
    company_name = Column(String(50))
    isin = Column(String(15))
    exchange_name = Column(String(30))

# Define the junction table to represent the many-to-many relationship
equity_tag = db.Table(
    'equity_tag',
    Column('equity_id', Integer, db.ForeignKey('equities.id')),
    Column('tag_id', Integer, db.ForeignKey('tags.id'))
)


class Equity(db.Model):
    __tablename__ = 'equities'
    id = Column(Integer, primary_key=True)
    token = Column(String(10))
    shortname = Column(String(30))
    company_name = Column(String(50))
    isin = Column(String(15))
    exchange_name = Column(String(30))
    # Define the many-to-many relationship with the "Tag" model
    tags = db.relationship('Tag', secondary=equity_tag, back_populates='equities', cascade="save-update")

class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tagname = Column(String(30))
    tag_description = Column(String(70))
    # Define the many-to-many relationship with the "Equity" model
    equities = db.relationship('Equity', secondary=equity_tag, back_populates='tags')
    