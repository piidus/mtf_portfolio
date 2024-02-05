from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from flask_mail import Mail
from flask_login import UserMixin
from flask_migrate import Migrate
from flask import abort
import datetime



mail = Mail()

db = SQLAlchemy()
migrate = Migrate()
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
    symbol = Column(String(10), nullable=True)
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
    orders = db.relationship('Order', backref='adv_order', lazy=True)

class Trigger(db.Model):
    table_name = 'triggers'
    id = Column(Integer, primary_key=True)
    date = Column(db.Date, default=datetime.datetime.today().date())
    time = Column(db.Time, default=datetime.datetime.today().time())
    strategy = Column(String(30), nullable = False)
    symbol = Column(String(30), nullable=True)
    token = Column(String(30), nullable=True)
    full_name = Column(String(100), nullable=True)
    isin = Column(String(15), nullable=True)
    target = Column(String(10), nullable=True)
    stop_loss = Column(String(10), nullable=True)
    ex1 = Column(String(30), nullable=True)
    ex2 = Column(String(30), nullable=True)
    ex3 = Column(String(30), nullable=True)
    ex4 = Column(String(30), nullable=True)
    ex5 = Column(String(30), nullable=True)
    ex6 = Column(String(30), nullable=True)
    ex7 = Column(String(30), nullable=True)
    ex8 = Column(String(30), nullable=True)
    ex9 = Column(String(30), nullable=True)

# Order Model
class Order(db.Model):
    table_name = "orders"
    id = db.Column(db.Integer, primary_key=True)
    # order_time =db.Column(db.DateTime, default = datetime.datetime.now)
    date = db.Column(db.Date, default=datetime.datetime.today().date())
    time = db.Column(db.Time, default=datetime.datetime.today().time())
    u_no = db.Column(db.String(70), nullable= False)
    exchange_id = db.Column(db.String(70), unique=True)
    exchange_code = db.Column(db.String(70))
    stock_name = db.Column(db.String(70))
    stock_token = db.Column(db.String(70))
    order_type = db.Column(db.String(70), nullable= True)
    action = db.Column(db.String(10), default = 'on') # on or off
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer, nullable = True)
    expiry = db.Column(db.String(30))
    strike_price = db.Column(db.String(30))
    right = db.Column(db.String(10))
    
    adv_order_id = db.Column(db.Integer, db.ForeignKey('advance_order.id'), nullable=True)

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
    company_name = Column(String(100))
    isin = Column(String(15))
    exchange_name = Column(String(30))
    # Define the many-to-many relationship with the "Tag" model
    tags = db.relationship('Tag', secondary=equity_tag, back_populates='equities', cascade="save-update")

class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tagname = Column(String(30))
    tag_description = Column(String(70))
    extra1 = Column(String(50))
    # Define the many-to-many relationship with the "Equity" model
    equities = db.relationship('Equity', secondary=equity_tag, back_populates='tags')

# OPtion Table
class OptionTable(db.Model):
    __table_name__ = 'optionstable'
    id = Column(Integer, primary_key=True)
    Token = Column(String(70))
    ShortName = Column(String(70))
    InstrumentName = Column(String(70))
    Series = Column(String(70))
    ExpiryDate =Column(String(70))
    StrikePrice = Column(String(70))
    LotSize = Column(String(70))




# for Second Database


def stock_table(table_name):

    metadata = MetaData()
    table = Table(table_name, metadata,
        Column('id', Integer, primary_key=True, autoincrement='auto'),
        Column('t_date',DateTime, unique=True),
        Column('open',Float),
        Column('high',Float),
        Column('low',Float),
        Column('close',Float),
        Column('volume', Integer),
        )   
    

    return table, metadata
