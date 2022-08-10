from flask import *
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

@app.route("/seeker_login" , methods=['GET', 'POST'])
def seeker_login():
    if request.method == "POST":
        loginDetails = request.form
        username = loginDetails['username']
        password = loginDetails['password']
        cursor = mysql.connection.cursor()
        cursor.execute("select * from seeker_loginData where username=%s and password=%s", (username, password,))
        details = cursor.fetchone()
        if details:
            session['loggedIn']= True
            session['username']= details[0]
            cursor.close()
            return redirect(url_for('home'))
        else:
            msg="Incorrrect Username/Password"
            cursor.close()
            return render_template("login.html", msg=msg)               
    return render_template("login.html")

@app.route("/seeker_signup" , methods=['GET', 'POST'])
def seeker_signup():
    if request.method == "POST":
        userDetails = request.form
        username = userDetails['username']
        user_email = userDetails['user_email']
        user_password = userDetails['user_password']
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

@app.route("/company_signup", methods=['GET', 'POST'])
def company_signup():
    if request.method=="POST":
        companyDetails = request.form
        username = companyDetails['username']
        companyName = companyDetails['companyName']
        companyEmail = companyDetails['companyEmail']
        companyCity = companyDetails['companyCity']
        password = companyDetails['password']
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

@app.route("/company_login", methods=['GET', 'POST'])
def company_login():
    if request.method == "POST":
        loginDetails = request.form
        username = loginDetails['username']
        password = loginDetails['password']
        cursor = mysql.connection.cursor()
        cursor.execute("select * from company_loginData where username=%s and password=%s", (username, password,))
        details = cursor.fetchone()
        if details:
            session['loggedIn']= True
            session['username']= details[0]
            cursor.close()
            return redirect(url_for('home'))
        else:
            msg="Incorrrect Username/Password"
            cursor.close()
            return render_template("login.html", msg=msg)               
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)