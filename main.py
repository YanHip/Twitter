from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import traceback
#from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/twitter"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#login_manager = LoginManager()
#login_manager.init_app(app)



class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<Users {self.username}>"


class MessageModel(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String())

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return f"<Message {self.message}>"


#db.create_all()


# Defining the home page of our site
@app.route('/home', methods=['GET', 'POST'])  # this sets the route to this page
def home():
    result = MessageModel.query.all()
    try:

        if request.method == 'POST':
            print(request.form['message'])

            message = MessageModel(message=request.form['message'])
            db.session.add(message)
            db.session.commit()
        else:
            print('ss')
    except:
        print(traceback.format_exc())

    return render_template('home.html', madata=result)  # some basic inline html

    #if connect:
    #else:
     #   return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = UsersModel.query.filter_by(username=request.form['username']).first()
        if user != None:
            if request.form['password'] != user.password:
                error = 'Invalid Credentials. Please try again.'
            else:
                return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/myfriends', methods=['GET'])
def friends():
    return render_template('myfriends.html')


@app.route('/privatemsg', methods=['GET'])
def privatemsg():
    return render_template('privatemsg.html')

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


if __name__ == "__main__":
    app.run()