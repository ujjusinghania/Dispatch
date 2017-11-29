from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
import pymysql.cursors
import hashlib
app = Flask(__name__)

# this is for pulling the port and database password from environment variables
import os

# Configure MySQL
conn = pymysql.connect(host='localhost',
                      port= int(os.environ['DB_PORT']), #get the port from an env var
                      user='root',
                      password= os.environ['DB_PASS'], #get the pswd from an env var
                      db='dispatch',
                      charset='latin1',
                      cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def login():
	return render_template('login.html')

@app.route('/home/friendgroups/messages', methods=['GET', 'POST'])
def messages():
	if (checkSess()):
		return redirect(url_for('login'))
	else:
		friendGroup = ( request.args.get("groupSelected"), request.args.get("username_creator") )
		print("friend group: {}{}".format(*friendGroup))
		session['groupSelected'] = friendGroup
		username = session['username']
		print(friendGroup)

		print("\n\n\nABOUT TO GET MESSAGES\n\n\n")
		messages = getMessages()
		print("\n\n\nJUST GOT MESSAGES\n\n\n")

		return render_template('messages.html', messages=messages)


@app.route('/home/friendgroups/getMessages')
def getMessages():
	cursor = conn.cursor()
		
	query = "SELECT Content.timest,									\
					Content.id as ContentID,						\
					Share.group_name,								\
			        Share.username as group_admin,					\
			        TextContent.text_content,						\
			        Content.username as ContentOwner,				\
			        Content.public									\
				FROM Share 											\
				JOIN Content ON Content.id = Share.id				\
			    JOIN TextContent on Content.id = TextContent.id 	\
			    WHERE group_name = %s  AND  Share.username = %s     "


	cursor.execute(query, session['groupSelected'])
	messages = cursor.fetchall() 

	cursor.close()

	print("\n\n\nIN GET_MESSAGES: {}\n\n\n".format(messages))

	# return messages
	return render_template('getMessages.html', messages=messages)


@app.route('/home/friendgroups', methods=['GET'])
def friendgroups():
	if (checkSess()):
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

		print(groups)
		cursor.close()

		return render_template('friendgroups.html', groups=groups)

@app.route('/home/tags',methods=['GET'])
def tags():
  username = session['username']
  cursor = conn.cursor()
  query = 'SELECT username_tagger, content_name FROM tags NATURAL JOIN content WHERE username_taggee = %s'
  cursor.execute(query,(username))
  tags =  cursor.fetchall()
  print(tag)
  cursor.close()

  return render_template('Tags.html',tags = tags)

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

@app.route('/settings/changepass')#, methods=['GET', 'POST'])
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


@app.route('/addMessage', methods = ['GET', 'POST'])
def addMessage():

	## There is an error in this. I use the current logged in user as the 
	## primary key for friendgroup, but it should be the group creator 

	message = request.form['userEnteredMessage']
	print(message)

	conn.commit()

	cursor = conn.cursor()
	query = 'INSERT INTO Content (username, content_name, public) VALUES(%s, %s, %s)'
	cursor.execute(query, (session['username'], "TextContent", False))


	query = 'INSERT INTO TextContent VALUES(LAST_INSERT_ID(), %s)'
	cursor.execute(query, (message))
	

								# content id, group name, group admin
	query = 'INSERT INTO Share VALUES(LAST_INSERT_ID(), %s, %s)'

	print(query, session['groupSelected'])

	cursor.execute(query, session['groupSelected'])



	query = 'SELECT * FROM Share WHERE id=LAST_INSERT_ID()'
	cursor.execute(query)

	data = cursor.fetchone()
	print(data)


	# query = 'SELECT * FROM Content NATURAL JOIN TextContent WHERE id=LAST_INSERT_ID()'
	# cursor.execute(query)
	
	# data = cursor.fetchone()
	# print(data)


	# commit changes and close connetion
	conn.commit()
	cursor.close()

	return redirect(url_for('messages')						+				
		'?groupSelected='+session['groupSelected'][0]		+
		'&username_creator='+session['groupSelected'][1]
		)


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

