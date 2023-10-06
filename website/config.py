import os, dotenv
dotenv.load_dotenv('.env')
DEBUG = True
# SQLALCHEMY_DATABASE_URI =
SECRET_KEY = 'hardsecretkey'
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
SQLALCHEMY_DATABASE_URI = f'mysql://{db_user}:{db_pass}@localhost:3306/{db_name}'
# 'mysql://username:password@localhost/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False