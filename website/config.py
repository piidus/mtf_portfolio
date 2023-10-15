import os, dotenv
dotenv.load_dotenv()
DEBUG = True
# from test import db, db_pwd, db_user1, db_path1
# SQLALCHEMY_DATABASE_URI =
SECRET_KEY = 'hardsecretkey'
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
db_path = os.environ.get('DB_PATH')
# SQLALCHEMY_DATABASE_URI = f'sqlite:///database.db'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_pass}@{db_path}:3306/{db_name}'
# SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user1}:{db_pwd}@{db_path1}:3306/{db}'
# 'mysql://username:password@localhost/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False