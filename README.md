# FindYourJob - Web App for Job Seekers and Recruiters

FindYourJob is a web application designed to assist both job seekers and recruiters in finding the ideal employment opportunities and candidates. This guide will walk you through the installation process for Linux.

## Installation Instructions

Follow these steps to set up FindYourJob on your Linux system:

### 1. Update Packages

First, update all your system packages:

```bash
sudo apt update
```

### 2. Install Git

Install Git using the following command:

```bash
sudo apt install git
```

### 3. Clone Repository

Clone the FindYourJob repository to your local machine:

```bash
git clone https://github.com/suyyash10/find_your_job
```

### 4. Install Python 3.10.5

Install Python 3.10.5 by executing the following commands:

```bash
cd /tmp/
wget https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tgz
tar -xzvf Python-3.10.5.tgz
cd Python-3.10.5/
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev
./configure --enable-optimizations
sudo make
sudo make install
```

### 5. Install Pip

Install Pip, the Python package manager:

```bash
sudo apt install python3-pip
```

### 6. Update Project Directory

Navigate to the project directory:

```bash
cd find_your_job
```

### 7. Update System

Update your system again:

```bash
sudo apt update
```

### 8. Install MySQL

Install MySQL server:

```bash
sudo apt install mysql-server
```

### 9. Configure MySQL

Access MySQL and update the root user password:

```bash
sudo mysql -u root -p
```

Inside MySQL, run the following query to enhance database connectivity:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '(new-password)';
```

Exit MySQL and restart the MySQL service:

```bash
exit
sudo service mysql restart
```

### 10. Install MySQL Client Library

Install the MySQL client library for Flask:

```bash
sudo apt-get install libmysqlclient-dev
```

### 11. Install Required Python Packages

Install the required Python packages using Pip:

```bash
pip install -r requirements.txt
```

### 12. Update MySQL Password

In the `app.py` file, replace the placeholder with your MySQL password for database connection.

### 13. Create MySQL Database

Execute all queries from the `queries_for_database_creation` file to create the necessary MySQL database.

### 14. Run the Application

Launch the FindYourJob app:

```bash
python3 app.py
```

The FindYourJob web application should now be up and running on your system.

