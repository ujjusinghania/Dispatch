from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
import pymysql.cursors
import hashlib
app = Flask(__name__)

# this is for pulling the port and database password from environment variables
import os

# Configure MySQL
conn = pymysql.connect(host='localhost',
                      port=int(os.environ['DB_PORT']),
                      user='root',
                      password=os.environ['DB_PASS'], #get the pswd from an env var
                      db='dispatch',
                      charset='latin1',
                      cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def login():
    return render_template('login.html')

#page that appears when you log in
def home():
    return render_template('index.html')
	
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	username = request.form['username']
	password = request.form['password']
	print(password)
	
	password_digest = md5(password)
	
	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s AND password = %s'
	cursor.execute(query, (username, password_digest))

	data = cursor.fetchone()
	print(data)
	cursor.close()

	if(data):
		return render_template('index.html')
	else:
		error = "Invalid Login or Username"
		return render_template('login.html', error=error)

@app.route('/register')
def register(): 
    return render_template('register.html')

@app.route('/registerAuth', methods = ['GET', 'POST'])
def registerAuth():
	print("hello")
	username = request.form['username']
	password = request.form['password']
	fname = request.form['fname']
	lname = request.form['lname']

	password_digest = md5(password)

	print("pswd_hash insert: ", password_digest)
	
	cursor = conn.cursor()
	query = 'INSERT INTO person VALUES (%s, %s, %s, %s)'
	cursor.execute(query, (username, password_digest, fname, lname))
	data = cursor.fetchone()
	
	print("\n\n\n")
	print(query, (username, password_digest, fname, lname))
	print(data)	
	print("\n\n\n")

	cursor.close()
	
	return render_template('login.html')
	#return "Welcome Home!"

def md5(password):
	m = hashlib.md5()
	password = password.encode('utf-8')
	m.update(password)
	password_digest = m.hexdigest()
	return password_digest

app.run()


'''
#change this
app.secret_key = "qwertyuiop"
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug=True)
'''