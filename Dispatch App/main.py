from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
from flask import Blueprint
import pymysql.cursors
from friends import friends_blueprint
from content import content_blueprint

import helpers

app = Flask(__name__)
app.register_blueprint(friends_blueprint)
app.register_blueprint(content_blueprint)

# this is for pulling the port and database password from environment variables
import os

# Configure MySQL
conn = pymysql.connect(host='localhost',
                      port= int(os.environ['DB_PORT']), #get the port from an env var
                      user='root',
                      password=os.environ['DB_PASS'], #get the pswd from an env var
                      db='dispatch',
                      charset='latin1',
                      cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def login():
	return render_template('login.html')


@app.route('/home/friendgroups', methods=['GET'])
def friendgroups():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		username = session['username']

		# Gets a list of all the groups the user is a part of/is the admin of.
		cursor = conn.cursor()
		query = 'SELECT DISTINCT group_name, username_creator 			\
						FROM member 									\
						WHERE username = %s OR username_creator = %s'

		cursor.execute(query, (username, username))
		groups = cursor.fetchall()

		# print(groups)
		cursor.close()

		return render_template('friendgroups.html', groups=groups)


@app.route('/home/tags', methods=['GET'])
def tag():
  username = session['username']
  cursor = conn.cursor()
  query = 'SELECT username_tagger \
  		   FROM tag\
  		   WHERE username_taggee = %s AND status = 0'

  cursor.execute(query, (username))
  tags = cursor.fetchall()
  cursor.close()
  return render_template('tags.html', tags=tags)

@app.route('/home/tags/acceptTag')
def acceptTag():
	taggedByUsername = request.args.get('taggedBy')
	taggedID = request.args.get('tagID')
	username = session['username']
	cursor = conn.cursor()
	query = 'DELETE FROM tag WHERE username_taggee = %s AND username_tagger = %s AND id = %d  AND status = FALSE'
	cursor.execute(query,(username,taggedByUsername,taggedID))
	query = 'INSERT INTO tag VALUES (%d,%s,%s,NULL,TRUE)'
	cursor.execute(query,(taggedID,username,taggedByUsername))
	conn.commit()
	cursor.close()
	return redirect(url_for('.tag'))

@app.route('/home/tags/declineTag')
def declineTag():
	taggedByUsername = request.args.get('taggedBy')
	taggedID = request.args.get('tagID')
	username = session['username']
	cursor = conn.cursor()
	query = 'DELETE FROM tag WHERE username_taggee = %s AND username_tagger = %s  AND status = FALSE'
	cursor.execute(query,(username,taggedByUsername))
	conn.commit()
	cursor.close()
	return redirect(url_for('.tag'))

@app.route('/logout')
def logout():
	#clear session variables
	session['username'] = ""
	session['fname'] = ""
	session['lname'] = ""
	session['color'] = ""
	return render_template('login.html', error="You have successfully logged out")


@app.route('/home')
def home():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('home.html')


@app.route('/home/settings')
def setting():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('settings.html', color=session['color'])


@app.route('/changecolor', methods=['GET', 'POST'])
def changecolor():
	col = request.args.get("favcolor")
	print(col)

	session['color'] = col

	cursor = conn.cursor()
	query = 'UPDATE person SET color = %s WHERE username = %s'
	cursor.execute(query, (session['color'], session['username']))
	conn.commit()

	return redirect(url_for('setting'))


@app.route('/settings/changepass')
def changepass():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		return render_template('changepass.html')


@app.route('/changePassAuth', methods=['GET', 'POST'])
def changepassAuth():
	currpass = request.form['current_password']
	newpass = request.form['new_password']
	confirmpass = request.form['confirm_password']

	current_password_digest = helpers.md5(currpass)

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
			new_password_digest = helpers.md5(newpass)
			confirm_password_digest = helpers.md5(confirmpass)

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

	password_digest = helpers.md5(password)

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
		session['color'] = data['color']     # color is in the person table now
		return redirect(url_for('home'))
	else:
		error = "Invalid Username or Password"
		return render_template('login.html', error=error)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	# get user input from form
	username = request.form['username']
	password = request.form['password']
	fname = request.form['fname']
	lname = request.form['lname']

	# hash the password
	password_digest = helpers.md5(password)

	# connonect to db and insert new user
	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	if(data):
		return render_template('register.html', error="Username already taken.")

	query = 'INSERT INTO person VALUES (%s, %s, %s, %s, %s)'
	cursor.execute(query, (username, password_digest, fname, lname, '#ea4c88'))
	data = cursor.fetchone()

	# commit changes and close connetion
	conn.commit()
	cursor.close()
	session['username'] = username
	session['fname'] = fname
	session['lname'] = lname
	session['color'] = '#ea4c88'
	return redirect(url_for('home'))


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
		conn.commit()
		return redirect(url_for('friendgroups'))

app.secret_key = os.urandom(24)
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug=True)
app.run()
