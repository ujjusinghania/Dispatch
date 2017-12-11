from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
from flask import Blueprint
import pymysql.cursors

import helpers

tags_blueprint = Blueprint('tags_blueprint', __name__)


# [temporary solution] This checks python version to decide what to import 
import sys
if sys.version_info[0] >= 3:
	import urllib.parse
else:
	import urllib
############################


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

@tags_blueprint.route('/home/tags', methods=['GET'])
def tag():
  username = session['username']
  cursor = conn.cursor()
  query = 'SELECT username_tagger,id \
  		   FROM tag\
  		   WHERE username_taggee = %s AND status = 0'

  cursor.execute(query, (username))
  tags = cursor.fetchall()
  cursor.close()
  print(tags)
  return render_template('tags.html', tags=tags)

@tags_blueprint.route('/home/tags/viewTags', methods=['GET'])
def viewTag():
  	username = session['username']
  	cursor = conn.cursor()
  	query = 'SELECT username_tagger,id \
  	FROM tag\
  	WHERE username_taggee = %s AND status = 1'

  	cursor.execute(query, (username))
  	tags = cursor.fetchall()
  	cursor.close()
  	print(tags)
  	return render_template('viewTags.html', tags=tags)

@tags_blueprint.route('/home/tags/acceptTag')
def acceptTag():
	taggedByUsername = request.args.get('taggedBy')
	taggedID = request.args.get('tagID')
	username = session['username']
	cursor = conn.cursor()
	query = 'DELETE FROM tag WHERE username_taggee = %s AND username_tagger = %s AND id = %s  AND status = FALSE'
	cursor.execute(query,(username,taggedByUsername,taggedID))
	query = 'INSERT INTO tag (username_taggee,username_tagger,id,status) VALUES (%s,%s,%s,TRUE)'
	cursor.execute(query,(username,taggedByUsername,taggedID))
	conn.commit()
	cursor.close()
	return redirect(url_for('.tag'))

@tags_blueprint.route('/home/tags/declineTag')
def declineTag():
	taggedByUsername = request.args.get('taggedBy')
	taggedID = request.args.get('tagID')
	username = session['username']
	cursor = conn.cursor()
	query = 'DELETE FROM tag WHERE username_taggee = %s AND username_tagger = %s AND id = %s AND status = FALSE'
	cursor.execute(query,(username,taggedByUsername,taggedID))
	conn.commit()
	cursor.close()
	return redirect(url_for('.tag'))


@tags_blueprint.route('/addTag', methods=['GET', 'POST'])
def addTag():
	cid = request.args.get('content_id')
	tagger = session['username']

	cursor = conn.cursor()
	query = 'SELECT first_name, last_name, username FROM ((SELECT first_name, last_name, username FROM friends JOIN person ON friends.friend_receive_username = person.username WHERE accepted_request = TRUE AND friend_send_username = %s) UNION (SELECT first_name, last_name, username FROM friends JOIN person ON friends.friend_send_username = person.username WHERE accepted_request = TRUE AND friend_receive_username = %s)) AS friends WHERE username NOT IN (Select username_taggee from tag where id = %s and username_tagger = %s)'
	cursor.execute(query,(tagger, tagger, cid, session['username']))
	possibleTags = cursor.fetchall()
	cursor.close()
	conn.commit()
	return render_template('addTags.html', possibleTags=possibleTags, content_id=cid)

@tags_blueprint.route('/addTag/auth', methods=['GET', 'POST'])
def addTagAuth():
	taggee = request.args.get('taggee')
	cid = request.args.get('cid')
	print(taggee, cid)
	cursor = conn.cursor()
	query = 'INSERT INTO tag (id, username_tagger, username_taggee) VALUES (%s, %s, %s)'
	cursor.execute(query, (cid, session['username'], taggee))
	conn.commit()

	return redirect(url_for('media_blueprint.medialibrary'))
