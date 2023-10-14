import os, dotenv
dotenv.load_dotenv('.env')
DEBUG = True
# SQLALCHEMY_DATABASE_URI =
SECRET_KEY = 'hardsecretkey'
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
db_path = os.getenv('DB_PATH')
# SQLALCHEMY_DATABASE_URI = f'sqlite:///database.db'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_pass}@{db_path}:3306/{db_name}'
# 'mysql://username:password@localhost/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False