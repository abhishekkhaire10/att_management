from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = 'hello'
# Configure db
db = yaml.load(open('config.ymal'), Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db['host']
app.config['MYSQL_USER'] = db['user']
app.config['MYSQL_PASSWORD'] = db['password']
app.config['MYSQL_DB'] = db['dbname']
app.config['MYSQL_PORT'] = db['port']

mysql = MySQL(app)

@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        loginDetails = request.form
        account_type = loginDetails['account']   
        if account_type == 'Admin':

            admin_name = loginDetails['name']
            admin_password = loginDetails['password']

            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM admin WHERE name = "'+admin_name+'"AND password = "'+admin_password+'"')
            result = cur.fetchall()

            if result:
                session['admin'] = admin_name
                flash("Youre Logged in", category='Success')
                return redirect(url_for('admin_homepage'))
            else:
                flash("Enter correct details", category='Success')
                return render_template('index.html')
        elif account_type == 'Student':
            student_name = loginDetails['name']
            student_password = loginDetails['password']

            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM student WHERE name = "'+student_name+'"AND password = "'+student_password+'"')
            result = cur.fetchall()

            if result:
                session['student'] = student_name
                flash("Youre Logged in", category='Success')
                return redirect(url_for('student_homepage'))
            else:
                flash("Enter correct details", category='Success')
                return render_template('index.html')
    return render_template('index.html')

@app.route('/admin_homepage', methods=['POST', 'GET'])
def admin_homepage():
    if 'admin' in session:
        admin_name = session['admin']
        return render_template('admin_homepage.html', admin_name = admin_name)
    else:
        flash("Please login to continue")
        return render_template('index.html')

@app.route('/student_homepage')
def student_homepage():
    if 'student' in session:
        student_name = session['student']
        return render_template('student_homepage.html', student_name = student_name)
    else:
        flash("Please login to continue")
        return render_template('index.html')

@app.route('/logout')
def logout():
    if 'admin' in session:
        session.pop('admin', None)
        flash("You're logged out")
        return redirect(url_for('index'))
    if 'student' in session:
        session.pop('student', None)
        flash("You're logged out")
        return redirect(url_for('index'))


# @app.route('/student_homepage<name>', methods=['POST', 'GET'])
# def student_homepage(name):
#     return render_template('student_homepage.html', name = name)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '8080')