from flask import Flask, render_template, flash, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
import os
#create the object of Flask
app  = Flask(__name__)

app.config['SECRET_KEY'] = 'hardsecretkey'
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_pass}@103.185.74.60:3306/{db_name}'

#SqlAlchemy Database Configuration With Mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskcodeloop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)


#our model
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))


    def __init__(self, username, password):
        self.username = username
        self.password = password







#creating our routes
@app.route('/')
def index():

    return render_template('index.html')



#login route
@app.route('/login' , methods = ['GET', 'POST'])
def Login():
    form = LoginForm()

    if form.validate_on_submit():
        if request.form['username'] != 'codeloop' or request.form['password'] != '12345':
            flash("Invalid Credentials, Please Try Again")


        else:
            return redirect(url_for('index'))



    return render_template('login.html', form = form)





#run flask app
if __name__ == "__main__":
    app.run(debug=True)