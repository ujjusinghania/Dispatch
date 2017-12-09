from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
from flask import Blueprint
import pymysql.cursors

import helpers

content_blueprint = Blueprint('content_blueprint', __name__)


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

@tag_blueprint.route('/home/tags', methods=['GET'])
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

@tag_blueprint.route('/home/tags/acceptTag')
def acceptTag():
	taggedByUsername = request.args.get('taggedBy')
	taggedID = request.args.get('tagID')
	username = session['username']
	cursor = conn.cursor()
	query = 'DELETE FROM tag WHERE username_taggee = %s AND username_tagger = %s AND id = %s  AND status = FALSE'
	cursor.execute(query,(username,taggedByUsername,taggedID))
	query = 'INSERT INTO tag VALUES (%s,%s,%s,NULL,TRUE)'
	cursor.execute(query,(taggedID,username,taggedByUsername))
	conn.commit()
	cursor.close()
	return redirect(url_for('.tag'))

@tag_blueprint.route('/home/tags/declineTag')
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


@tag_blueprint.route('/addTag',methods=['POST'])
def addTag():
	content_id = request.args.get('content_id')
	username = request.form['taggee_name']

	conn.commit()

	cursor = conn.cursor()
	query = 'INSERT INTO tag (id,username_tagger,username_taggee,status) VALUES (%s,%s,%s, False)'
	cursor.execute(query,(content_id,username,session['username']))

	conn.commit()
	return redirect(url_for('.medialibrary'))
