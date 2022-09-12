# find_your_job
FindYourJob is a web-app that helps jobs seekers and recruiters to find the perfect job and employees.

Installation Instructions For Linux:
1. First update all packages.
2. Install git with "sudo apt install git".
3. Import the Repository in your computer with command "git clone https://github.com/suyyash10/find_your_job"
4. For installing Python 3.10.5 run the following commands in given order in a new terminal:
    1. cd /tmp/
    2. wget https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tgz
    3. tar -xzvf Python-3.10.5.tgz
    4. cd Python-3.10.5/
    5. sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev
    6. ./configure --enable-optimizations
    7. sudo make
    8. sudo make install

5. Install pip with command "sudo apt install python3-pip"
6. Open a new terminal and type command "cd find_your_job" and type command "sudo apt update".
7. Install mysql with "sudo apt install mysql-server"
8. Run mysql with "sudo mysql -u root -p" and type your linux password.
9. Run this query in mysql to avoid complecations in database connectivity "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new-password';"
10. Now exit mysql and run this command "sudo service mysql restart"
11. Now run this command for flask_mysqldb package in python "sudo apt-get install libmysqlclient-dev"
12. Install the required python packages with command "pip install -r requirements.txt"
13. In app.py, update the mysql password with your current password.
14. For mysql database creation, run all the queries in the "queries_for_database_creation" file.
15. run the project with command "python3 app.py".




