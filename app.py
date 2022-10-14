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
import random

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

'''

#function to check if a table exist in the database
def check_table(name):
    cursor = mysql.connection.cursor()
    #exist = cursor.execute("select * from %s", (tname,))
    #exist = cursor.fetchone()[0]
    cursor.execute("show tables")
    test = cursor.fetchall()
    cursor.close()
    if name in test:
        return 1
    return 0

#Home page
@app.route("/")
def home():
    session.clear()
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
        if details:
            test = details[1]
            test = test.encode()
            test = f.decrypt(test)
            test = test.decode()
        else:
            return render_template("login.html") 
        if details and test == password:
            session['loggedIn']= True
            session['username']= details[0]
            cursor.close()
            return redirect(url_for('seeker_profile'))
        else:
            
            msg="Incorrrect Username/Password"
            cursor.close()
            return render_template("login.html", msg=msg )               
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
        cursor.execute("select * from seeker_loginData where username=%s", (username,))
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
        user_password = userDetails['user_password1']
        user_password = user_password.encode()
        user_password = f.encrypt(user_password)
        user_password = user_password.decode()
        cursor = mysql.connection.cursor()
        cursor.execute("select username from seeker_loginData where username = %s", (username,))
        test = cursor.fetchone()
        if not test:
            cursor.execute("insert into seeker_basicData(username,email) values(%s, %s)", (username, user_email))
            cursor.execute("insert into seeker_loginData values(%s, %s)", (username, user_password))
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
        name = details['fullname']
        gender = details['gender']
        dob = details['dob']
        education = details['education']
        skills = details['skills']
        '''phone = details['phoneno']'''
        address = details['address']
        post = details['post']
        username = session['username']
        cursor = mysql.connection.cursor()
        cursor.execute("update seeker_basicData set full_name=%s, gender=%s, dob=%s, education=%s, skills=%s, address=%s, post=%s where username=%s", (name, gender, dob, education, skills, address, post, username))
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
        cursor.execute("select * from company_loginData where username = %s", (username,))
        test = cursor.fetchone()
        if not test:
            cursor.execute("insert into company_basicData values(%s, %s, %s, %s)", (username, companyName, companyEmail, companyCity))
            cursor.execute("insert into company_loginData values(%s, %s)", (username, password))
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
        cursor.execute("select * from company_loginData where username=%s", (username,))
        details = cursor.fetchone()
        test = details[1]
        test = test.encode()
        test = f.decrypt(test)
        test = test.decode()
        if details and test == password:
            session['loggedIn']= True
            session['username']= details[0]
            cursor.close()
            return redirect(url_for('recruiter_profile'))
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
    usrpost = basicdata[6]
    education = basicdata[5]
    skill = basicdata[6]
    cursor.execute("select * from jobs where skills=%s", (skill,))
    alljobs = cursor.fetchall()
    if request.method == "POST":
        id = request.form["action"]
        id = str(id)
        tablename = "job"+id
        query = "insert into "+tablename
        cursor.execute(query+" values(%s, %s, %s)", (name, email, education))
        mysql.connection.commit()
    cursor.close()
    return render_template("seeker_profile.html",alljobs=alljobs, name=name, email=email, usrpost=usrpost)

#Recruiter Profile
@app.route("/recruiter_profile", methods=['GET', 'POST'])
def recruiter_profile():
    cursor = mysql.connection.cursor()
    cursor.execute("select company_name from company_basicdata where username = %s", (session["username"],))
    comp = cursor.fetchone()
    comp = comp[0] 
    cursor.execute("select * from jobs where Company=%s", (comp,))
    alljobs = cursor.fetchall()
    cursor.execute("select * from company_basicData where username = %s", (session['username'],))
    data = cursor.fetchone()
    if request.method == "POST":
        jobId = request.form["action"]
        session["jobId"]=jobId
        return redirect(url_for('screening'))
        cursor.close()
    cursor.close()
    return render_template("job_giver.html", alljobs=alljobs, data=data)

#Add Job
@app.route("/add_job", methods=['GET', 'POST'])
def add_job():
    cursor = mysql.connection.cursor()
    cursor.execute("select * from company_basicData where username = %s", (session['username'],))
    data = cursor.fetchone()
    name = data[1]
    email = data[2]
    username = data[0]
    if request.method == "POST":
        while true:
            num = random.randint(100000, 999999)
            cursor.execute("select * from jobs where jobID = %s", (num, ))
            test=cursor.fetchone()
            if test:
                continue
            else:
                break
        num = str(num)
        query = "create table job"+num+" (emp_name varchar(100) primary key, emp_email varchar(50), emp_education varchar(50))"
        cursor.execute(query)
        details= request.form
        description = details['description']
        post = details['keyword']
        #exp = details['experience']
        salary = details['salary']
        skills = details['skills']
        location = details['location']
        tablename = session["username"]
        cursor.execute("insert into jobs values(%s, %s, %s, %s, %s, %s, %s)", (num, post, description, name, salary, location, skills,))
        mysql.connection.commit()
        cursor.close()
        return redirect("recruiter_profile")
    cursor.close()
    return render_template("add_job.html", name=name, email=email, username=username)

#Screening
@app.route("/screening", methods=["GET", "POST"])
def screening():
    cursor = mysql.connection.cursor()
    jobId = session['jobId']
    tablename = "job"+jobId
    query = "select * from "+tablename
    cursor.execute(query)
    allreq = cursor.fetchall()
    return render_template("screening.html", allreq = allreq)


if __name__ == "__main__":
    app.run(debug=True)