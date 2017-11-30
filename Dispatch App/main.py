from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
import pymysql.cursors
import hashlib

app = Flask(__name__)

# this is for pulling the port and database password from environment variables
import os

# Configure MySQL
conn = pymysql.connect(host='localhost',
                      #port= int(os.environ['DB_PORT']), #get the port from an env var
                      user='root',
                      password='',#os.environ['DB_PASS'], #get the pswd from an env var
                      db='dispatch',
                      charset='latin1',
                      cursorclass=pymysql.cursors.DictCursor)

conn.autocommit = True

@app.route('/')
def login():
	return render_template('login.html')

@app.route('/home/friendgroups/messages', methods=['GET'])
def messages():
	if (checkSess()):
		return redirect(url_for('login'))
	else:
		friendGroup = request.args.get("groupSelected")
		print("friend group: "+friendGroup)
		session['groupSelected'] = friendGroup
		username = session['username']
		print(friendGroup)

		cursor = conn.cursor()
		# Gets a list of all the content that the user has posted/is public. 
		# Need to add list of content that is shared with groups the user is a part of. 
		query = 'SELECT * FROM share NATURAL JOIN content WHERE group_name = %s AND (username = %s OR public = 1)'
		cursor.execute(query, (username, friendGroup))
		messages = cursor.fetchall() 
		print(messages)

		cursor.close()

		return render_template('messages.html')

@app.route('/home/friendgroups', methods=['GET'])
def friendgroups():
	if (checkSess()):
		return redirect(url_for('login'))
	else:
		username = session['username']

		# Gets a list of all the groups the user is a part of/is the admin of. 
		cursor = conn.cursor()
		query = 'SELECT DISTINCT group_name FROM member WHERE username = %s OR username_creator = %s'
		cursor.execute(query, (username, username))
		groups = cursor.fetchall()
		print(groups)
		cursor.close()
		return render_template('friendgroups.html', groups=groups)

@app.route('/home/tags',methods=['GET'])
def tag():
  username = session['username']
  cursor = conn.cursor()
  query = 'SELECT username_taggee, content_name FROM tag NATURAL JOIN content WHERE username_taggee = %s'
  cursor.execute(query,(username))
  tag =  cursor.fetchall()
  print(tag)
  cursor.close()
  return render_template('tags.html',tags = tag)

def checkSess():
	return (session['username'] == "" and session['fname'] == "" and session['lname'] == "")
	
@app.route('/logout')
def logout():
	#clear session variables
	session['username'] = ""
	session['fname'] = ""
	session['lname'] = ""
	return render_template('login.html', error="You have successfully logged out")

def checkSess():
	return (session['username'] == "" and session['fname'] == "" and session['lname'] == "")
	
@app.route('/home')
def home():
	if (checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('home.html')

@app.route('/home/settings')
def setting():
	if (checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('settings.html')

@app.route('/settings/changecolor')
def changecolor():		
	if (checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('changecolor.html')

@app.route('/changecolorAuth')
def changecolorAuth():
	pass
		
@app.route('/settings/changepass')
def changepass():
	if (checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('changepass.html')
		
@app.route('/changePassAuth', methods=['GET', 'POST'])
def changepassAuth():
	currpass = request.form['current_password']
	newpass = request.form['new_password']
	confirmpass = request.form['confirm_password']

	current_password_digest = md5(currpass)
	
	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s AND password = %s'
	cursor.execute(query, (session['username'], current_password_digest))

	data = cursor.fetchone()
	print(data)
	cursor.close()
	
	if (data):
		if (newpass != confirmpass):
			error = "Passwords Do Not Match"
			print(error)
			return render_template('changepass.html', error=error)
		else:
			new_password_digest = md5(newpass)
			confirm_password_digest = md5(confirmpass)
			
			cursor = conn.cursor()
			query = 'UPDATE person SET password = %s WHERE username = %s'
			cursor.execute(query, (new_password_digest, session['username']))
			conn.commit()
			
			query = 'SELECT * FROM person WHERE username = %s AND password = %s'
			cursor.execute(query, (session['username'], new_password_digest))
			
			data1 = cursor.fetchone()
			print(data1)
			cursor.close()
			return redirect(url_for('setting'))
	else:
		error = "Incorrect Password"
		print(error)
		return render_template('changepass.html', error=error)
		
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	username = request.form['username']
	password = request.form['password']
	
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
	query = 'SELECT * FROM person WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	if(data):
		return render_template('register.html', error="Username already taken.")

	query = 'INSERT INTO person VALUES (%s, %s, %s, %s)'
	cursor.execute(query, (username, password_digest, fname, lname))
	data = cursor.fetchone()
	
	# commit changes and close connetion
	conn.commit()
	cursor.close()
	session['username'] = username
	session['fname'] = fname
	session['lname'] = lname
	return redirect(url_for('home'))
	#return "Welcome Home!"

@app.route('/home/friendgroups/addfriendgroup')
def addFriendGroup(): 
	return render_template('addfriendgroup.html')

@app.route('/home/friendgroups/addfriendgroup/addtodatabase', methods=['GET', 'POST'])
def addFriendGroupAuth(): 
	cursor = conn.cursor()

	groupName = request.form['group_name']
	groupDescription = request.form['group_description']
	username = session['username']

	query = 'SELECT username, group_name FROM friendgroup WHERE username = %s AND group_name = %s'
	cursor.execute(query, (username, groupName))
	data = cursor.fetchone()
	if (data):
		return render_template('addfriendgroup.html', error="You already own a FriendGroup called " + groupName)
	else:
		query = 'INSERT INTO friendgroup VALUES(%s, %s, %s)'
		cursor.execute(query, (groupName, username, groupDescription))
		query = 'INSERT INTO member VALUES(%s, %s, %s)'
		cursor.execute(query, (username, groupName, username))
		return redirect(url_for('friendgroups'))
		conn.commit()

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

