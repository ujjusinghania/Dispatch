from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
import pymysql.cursors

app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                      port=8889,
                      user='root',
                      password='root',
                      db='dispatch',
                      charset='latin1',
                      cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	username = request.form['username']
	password = request.form['password']
	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s AND password = %s'
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	cursor.close()

	if(data):
		session['username'] = username
		return redirect(url_for('home'))
	else:
		error = "Invalid Login or Username"
		return render_template('login.html', error=error)

@app.route('/register')
def register(): 
    return render_template('register.html')

@app.route('/registerAuth', methods = ['GET', 'POST'])
def registerAuth():
    return "Welcome Home!"

app.run()

'''
#change this
app.secret_key = "qwertyuiop"
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug=True)
'''
