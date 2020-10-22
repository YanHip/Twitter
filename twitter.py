from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="dev",
        password="dev",
        host="192.168.53.135",
        port=3306,
        database="api_dl"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

app = Flask(__name__)

#login_manager = LoginManager()
#login_manager.init_app(app)

# Defining the home page of our site
@app.route("/home")  # this sets the route to this page
def home():
    #if connect:
        cur.execute("SELECT * FROM files")
        list = []
        for line in cur:
            list.append(line)

        return render_template('home.html', madata = list) # some basic inline html
    #else: 
     #   return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home')), connect

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