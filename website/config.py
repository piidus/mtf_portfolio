import os
# import dotenv
# dotenv.load_dotenv()
DEBUG = True
# from test import db, db_pwd, db_user1, db_path1

# SQLALCHEMY_DATABASE_URI =
SECRET_KEY = 'hardsecretkey'
db_user = os.environ.get('DB_USER')
db_user_pass = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
db_path = os.environ.get('DB_PATH')
# mail server configuration
mail_pwd = os.environ.get('MAIL_PWD')
MAIL_SERVER='mtf.piidus.in'
MAIL_PORT = 587
MAIL_USERNAME = 'info@mtf.piidus.in'
MAIL_PASSWORD = mail_pwd
MAIL_USE_TLS = True
MAIL_USE_SSL = False
# print('MAIL PWD :', db_user)
# SQLALCHEMY_DATABASE_URI = f'sqlite:///database.db'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_user_pass}@{db_path}:3306/{db_name}'
# SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user1}:{db_pwd}@{db_path1}:3306/{db}'
# 'mysql://username:password@localhost/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# git update-index --assume-unchanged website/config.py
# To update
# git update-index --no-assume-unchanged website/config.py
 