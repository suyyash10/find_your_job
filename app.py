from flask import *
from flask_mysqldb import * 
from sqlalchemy import *
import mysql.connector

app = Flask(__name__)

#database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'findmyjob'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup" , methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        userDetails = request.form
        username = userDetails['username']
        user_email = userDetails['user_email']
        user_password = userDetails['user_password']
        cursor = mysql.connection.cursor()
        cursor.execute("insert into BasicData values(%s, %s,%s)", (username, user_email, user_password))
        cursor.execute("insert into loginData values(%s, %s)", (username, user_password))
        mysql.connection.commit()
        cursor.close()

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)