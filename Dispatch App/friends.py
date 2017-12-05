from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
from flask import Blueprint
import pymysql.cursors
import hashlib

friends_blueprint = Blueprint('friends_blueprint',__name__)

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

@friends_blueprint.route('/home/friendhome')
def viewFriendHome():
	return render_template('friendhome.html')

@friends_blueprint.route('/home/friendhome/addfriend')
def addFriend():
	return render_template('addfriend.html')

@friends_blueprint.route('/home/friendhome/friendrequest')
def viewFriendRequests():
	username = session['username']
	cursor = conn.cursor()

	# Finding friends who you received a friend request from. 
	query = 'SELECT first_name, last_name, username FROM friends JOIN person ON friends.friend_send_username = person.username WHERE accepted_request = FALSE AND friend_receive_username = %s'
	cursor.execute(query, (username))
	frequests = cursor.fetchall()
	cursor.close()
	return render_template('friendrequests.html', friendRequests=frequests)
	
@friends_blueprint.route('/home/friendhome/viewfriends')
def viewFriends():
	username = session['username']
	cursor = conn.cursor()

	# Finding friends who you sent a friend request to. 
	query = 'SELECT first_name, last_name, username FROM friends JOIN person ON friends.friend_receive_username = person.username WHERE accepted_request = TRUE AND friend_send_username = %s'
	cursor.execute(query, (username))
	requestSendFriends = cursor.fetchall()

	# Finding friends who you received a friend request from. 
	query = 'SELECT first_name, last_name, username FROM friends JOIN person ON friends.friend_send_username = person.username WHERE accepted_request = TRUE AND friend_receive_username = %s'
	cursor.execute(query, (username))
	requestReceiveFriends = cursor.fetchall()
	cursor.close()

	allFriends = []
	for friend in requestReceiveFriends:
		allFriends.append(friend)
	for friend in requestSendFriends:
		allFriends.append(friend)	

	return render_template('viewfriends.html', friends=allFriends)
	
@friends_blueprint.route('/home/friendhome/addfriend/acceptRequest')
def acceptFriendRequest():
	sentByUsername = request.args.get('sentBy')
	username = session['username']
	cursor = conn.cursor()
	query = 'DELETE FROM friends WHERE friend_send_username = %s AND friend_receive_username = %s AND accepted_request = FALSE'
	cursor.execute(query, (sentByUsername, username))
	query = 'INSERT INTO friends VALUES(%s, %s, TRUE)'
	cursor.execute(query, (sentByUsername, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('.viewFriendRequests'))

@friends_blueprint.route('/home/friendhome/addfriend/declineRequest')
def declineFriendRequest():
	sentByUsername = request.args.get('sentBy')
	username = session['username']
	cursor = conn.cursor()
	query = 'DELETE FROM friends WHERE friend_send_username = %s AND friend_receive_username = %s AND accepted_request = FALSE'
	cursor.execute(query, (sentByUsername, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('.viewFriendRequests'))
