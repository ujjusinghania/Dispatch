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

# Functions pertaining to addition/deletion/viewing of Friends on the App. 

@app.route('/home/friendhome')
def viewFriendHome():
	return render_template('friendhome.html')

@app.route('/home/friendhome/addfriend')
def addFriend():
	return render_template('addfriend.html')

@app.route('/home/friendhome/viewfriends')
def viewFriends():
	username = session['username']
	cursor = conn.cursor()

	# Finding friends who you sent a friend request to. 
	query = 'SELECT first_name, last_name FROM friends JOIN person ON friends.friend_send_username = person.username WHERE accepted_request = TRUE AND friend_receive_username = %s'
	cursor.execute(query, (username))
	requestSendFriends = cursor.fetchall()

	# Finding friends who you received a friend request from. 
	query = 'SELECT first_name, last_name FROM friends JOIN person ON friends.friend_receive_username = person.username WHERE accepted_request = TRUE AND friend_send_username = %s'
	cursor.execute(query, (username))
	requestReceiveFriends = cursor.fetchall()

	return render_template('viewfriends.html', friends=requestReceiveFriends+requestSendFriends)

@app.route('/home/friendhome/friendrequest')
def viewFriendRequests():
	return render_template('friendrequest.html')

app.secret_key = os.urandom(24)
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
app.run()