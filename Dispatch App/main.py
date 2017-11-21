from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
import pymysql.cursors
import hashlib
app = Flask(__name__)

# this is for pulling the port and database password from environment variables
import os

# Configure MySQL
conn = pymysql.connect(host='localhost',
                      port=int(os.environ['DB_PORT']), #get the port from an env var
                      user='root',
                      password=os.environ['DB_PASS'],#'root', #get the pswd from an env var
                      password= os.environ['DB_PASS'], #get the pswd from an env var
                      db='dispatch',
                      charset='latin1',
                      cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def login():
	return render_template('login.html')

@app.route('/home/friendgroups')
def friendgroups():
	username = session['username']

	# Gets a list of all the groups the user is a part of/is the admin of. 
	cursor = conn.cursor()
	query = 'SELECT DISTINCT group_name FROM member WHERE username = %s OR username_creator = %s'
	cursor.execute(query, (username, username))
	groups = cursor.fetchall()
	print(groups)
	cursor.close()
	
	return render_template('friendgroups.html', groups=groups)

@app.route('/home')
def home():
	# # Gets a list of all the content that the user has posted/is public. 
	# # Need to add list of content that is shared with groups the user is a part of. 
	# query = 'SELECT * FROM content WHERE username = %s OR public = 1'
	# cursor.execute(query, (username))
	# messages = cursor.fetchall() 
	# print(groups)

	# cursor.close()

	return render_template('home.html')

	
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
		session['username'] = username
		session['fname'] = data['first_name']
		session['lname'] = data['last_name']
		return redirect(url_for('home'))
	else:
		error = "Invalid Username or Password"
		return render_template('login.html', error=error)


@app.route('/register')
def register(): 
    return render_template('register.html')


@app.route('/registerAuth', methods = ['GET', 'POST'])
def registerAuth():
	# get user input from form
	username = request.form['username']
	password = request.form['password']
	fname = request.form['fname']
	lname = request.form['lname']

	# hash the password
	password_digest = md5(password)

	# connonect to db and insert new user
	cursor = conn.cursor()
	query = 'INSERT INTO person VALUES (%s, %s, %s, %s)'
	cursor.execute(query, (username, password_digest, fname, lname))
	data = cursor.fetchone()
	
	# commit changes and close connetion
	conn.commit()
	cursor.close()
	if(data):
		return render_template('register.html', error="Username already taken.")
	else:
		session['username'] = username
		session['fname'] = data['first_name']
		session['lname'] = data['last_name']
		return redirect(url_for('home'))
	#return "Welcome Home!"


def md5(password):
	# encode and hash password
	m = hashlib.md5()
	password = password.encode('utf-8')
	m.update(password)
	password_digest = m.hexdigest()
	return password_digest

app.secret_key = os.urandom(24)
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
app.run()

