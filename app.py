from flask import Flask, request, render_template, url_for, session, redirect
from flask_mysqldb import *
from sqlalchemy import *
import mysql.connector

app = Flask(__name__)
app.secret_key="mykey"

#database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'findmyjob'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login" , methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        loginDetails = request.form
        username = loginDetails['username']
        password = loginDetails['password']
        cursor = mysql.connection.cursor()
        cursor.execute("select * from loginData where username=%s and password=%s", (username, password,))
        details = cursor.fetchone()
        if details:
            session['loggedIn']= True
            session['username']= details[0]
            return redirect(url_for('home'))
        else:
            msg="Incorrrect Username/Password"
            return render_template("login.html", msg=msg)               
        cursor.close()
    return render_template("login.html")

@app.route("/signup" , methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        userDetails = request.form
        username = userDetails['username']
        user_email = userDetails['user_email']
        user_password = userDetails['user_password']
        cursor = mysql.connection.cursor()
        cursor.execute("select username from loginData where username = %s", (username,))
        test = cursor.fetchone()
        if not test:
            cursor.execute("insert into BasicData values(%s, %s)", (username, user_email))
            cursor.execute("insert into loginData values(%s, %s)", (username, user_password))
        mysql.connection.commit()
        cursor.close()

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)