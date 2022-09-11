from flask import *
from flask_mysqldb import *
from cryptography.fernet import Fernet
from sqlalchemy import *
'''from google_auth_oauthlib import *
from google_auth_oauthlib.flow import *
from oauthlib import *
import os
import pathlib'''
import mysql.connector

#Flask app configuration
app = Flask(__name__)
app.secret_key="mykey"

file = open('key.key', 'rb')
key = file.read()
file.close()
f = Fernet(key)
'''
google_client_id = "51389405275-h4qp9neamc2bitlc8h0h6lfcpor8ba8d.apps.googleusercontent.com"

client_secret_file= os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=["https://www.googleapis.com/userinfo.profile", "https://googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1;5000/")
'''
#database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'findmyjob'

mysql = MySQL(app)
'''
#decorator for protection
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            abort(401)
        else:
            return function
    return wrapper


#Class for Data Retrival form database
class Jobs(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("select Company from jobs")
    company = cursor.fetchall()
    cursor.clear()
    cursor.execute("select post from jobs")
    post = cursor.fetchall()
    cursor.clear()
    cursor.execute("select Description from jobs")
    description = cursor.fetchall()
    cursor.clear()
    cursor.execute("select Recruiter_Name from jobs")
    reqName = cursor.fetchall()
    cursor.clear()
    cursor.execute("select Recruiter_Post from jobs")
    reqPost = cursor.fetchall()
    cursor.clear()
'''

#Home page
@app.route("/")
def home():
    return render_template("home.html")

#Seeker Login function
@app.route("/seeker_login" , methods=['GET', 'POST'])
def seeker_login():
    if request.method == "POST":
        loginDetails = request.form
        username = loginDetails['username']
        password = loginDetails['password']
        cursor = mysql.connection.cursor()
        cursor.execute("select * from seeker_loginData where username=%s", (username,))
        details = cursor.fetchone()
        test = details[1]
        test = test.encode()
        test = f.decrypt(test)
        test = test.decode()
        if details and test == password:
            session['loggedIn']= True
            session['username']= details[0]
            cursor.close()
            return redirect(url_for('seeker_profile'))
        else:
            msg="Incorrrect Username/Password"
            cursor.close()
            return render_template("login.html", msg=msg)               
    return render_template("login.html")

#Seeker Google Login function
'''
@app.route("/seeker_googlelogin", methods=["GET", "POST"])
def seeker_googlelogin():
    if request.method == "POST":
        details = request.form
        username = details['username']
        password = details['password']
        cursor = mysql.connection.cursor()
        cursor.execute("select * from seeker_logindata where username=%s", (username,))
        test = cursor.fetchone()
        if not test:
            authorization_url, state= flow.authorization_url()
            session["state"]= state
            return redirect(authorization_url)
    return render_template("seeker_googlelogin.html")
'''

#Seeker Signup function
@app.route("/seeker_signup" , methods=['GET', 'POST'])
def seeker_signup():
    if request.method == "POST":
        userDetails = request.form
        username = userDetails['username']
        user_email = userDetails['user_email']
        user_password = userDetails['user_password']
        user_password = user_password.encode()
        user_password = f.encrypt(user_password)
        user_password = user_password.decode()
        cursor = mysql.connection.cursor()
        cursor.execute("select username from seeker_loginData where username = %s", (username,))
        test = cursor.fetchone()
        if not test:
            cursor.execute("insert into seeker_basicdata(username,email) values(%s, %s)", (username, user_email))
            cursor.execute("insert into seeker_logindata values(%s, %s)", (username, user_password))
            mysql.connection.commit()
            cursor.close()
            session['username'] = username
            return redirect('seeker_details')
        cursor.close()
    return render_template("seeker_signup.html")

#Seeker Details Entries function
@app.route("/seeker_details" , methods=['GET', 'POST'])
def seeker_details():
    if request.method == "POST":
        details = request.form
        name = details['fullName']
        company = details['companyName']
        designation = details['designation']
        experience = details['experience']
        username = session['username']
        cursor = mysql.connection.cursor()
        cursor.execute("update seeker_basicdata set full_name=%s, current_company=%s, current_designation=%s, job_experience=%s where username=%s", (name, company, designation, experience, username))
        mysql.connection.commit()
        cursor.close()
        return redirect('seeker_login')
    return render_template("seeker_details.html")

#Company Signup function
@app.route("/company_signup", methods=['GET', 'POST'])
def company_signup():
    if request.method=="POST":
        companyDetails = request.form
        username = companyDetails['username']
        companyName = companyDetails['companyName']
        companyEmail = companyDetails['companyEmail']
        companyCity = companyDetails['companyCity']
        password = companyDetails['password']
        password = password.encode()
        password = f.encrypt(password)
        password = password.decode()
        cursor =mysql.connection.cursor()
        cursor.execute("select * from company_logindata where username = %s", (username,))
        test = cursor.fetchone()
        if not test:
            cursor.execute("insert into company_basicdata values(%s, %s, %s, %s)", (username, companyName, companyEmail, companyCity))
            cursor.execute("insert into company_logindata values(%s, %s)", (username, password))
            mysql.connection.commit()
            cursor.close()
            return redirect('company_login')
        cursor.close()
    return render_template("company_signup.html")

#Company Login function
@app.route("/company_login", methods=['GET', 'POST'])
def company_login():
    if request.method == "POST":
        loginDetails = request.form
        username = loginDetails['username']
        password = loginDetails['password']
        cursor = mysql.connection.cursor()
        cursor.execute("select * from company_loginData where username=%s and password=%s", (username, password,))
        details = cursor.fetchone()
        test = details[1]
        test = test.encode()
        test = f.decrypt()
        test = test.decode()
        if details and test == password:
            session['loggedIn']= True
            session['username']= details[0]
            cursor.close()
            return redirect(url_for('home'))
        else:
            msg="Incorrrect Username/Password"
            cursor.close()
            return render_template("login.html", msg=msg)               
    return render_template("login.html")

#Seeker Profile function
@app.route("/user_profile", methods=['GET', 'POST'])
def seeker_profile():
    username = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute("select * from seeker_basicData where username=%s", (username,))
    basicdata = cursor.fetchone()
    name = basicdata[2]
    email = basicdata[1]
    usrpost = basicdata[4]
    '''cursor.execute("select count(*) from jobs")
    number = cursor.fetchone()
    number = int(number[0])
    cursor.execute("select Company from jobs")
    company = cursor.fetchall()
    cursor.execute("select post from jobs")
    post = cursor.fetchall()
    cursor.execute("select Description from jobs")
    description = cursor.fetchall()
    cursor.execute("select Recruiter_Name from jobs")
    reqName = cursor.fetchall()
    cursor.execute("select Recruiter_Post from jobs")
    reqPost = cursor.fetchall()'''
    cursor.execute("select * from jobs")
    alljobs = cursor.fetchall()
    cursor.close()

    return render_template("seeker_profile.html",alljobs=alljobs, name=name, email=email, usrpost=usrpost)

if __name__ == "__main__":
    app.run(debug=True)