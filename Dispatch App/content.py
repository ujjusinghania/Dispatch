from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
from flask import Blueprint
import pymysql.cursors

import helpers

content_blueprint = Blueprint('content_blueprint',__name__)

# [temporary solution] This checks python version to decide what to import 
import sys
if sys.version_info[0] >= 3:
	import urllib.parse
else:
	import urllib
################################


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

# Functions pertaining to content


@content_blueprint.route('/addMessage', methods=['GET', 'POST'])
def addMessage():

	message = request.form['userEnteredMessage']
	# print(message)

	conn.commit()

	cursor = conn.cursor()
	query = 'INSERT INTO Content (username, content_name, public) VALUES(%s, %s, %s)'
	cursor.execute(query, (session['username'], "TextContent", False))

	query = 'INSERT INTO TextContent VALUES(LAST_INSERT_ID(), %s)'
	cursor.execute(query, (message))

	# content id, group name, group admin
	query = 'INSERT INTO Share VALUES(LAST_INSERT_ID(), %s, %s)'

	cursor.execute(query, session['groupSelected'])

	query = 'SELECT * FROM Share WHERE id=LAST_INSERT_ID()'
	cursor.execute(query)

	data = cursor.fetchone()

	# commit changes and close connetion
	conn.commit()
	cursor.close()

	return redirect(url_for('messages') +
                 '?groupSelected=' + session['groupSelected'][0] +
                 '&username_creator=' + session['groupSelected'][1]
                 )

@content_blueprint.route('/addPhoto', methods=['GET', 'POST'])
def addPhoto():

	url = urllib.parse.quote_plus( request.form['photo_url'] )
	# print(message)

	conn.commit()

	cursor = conn.cursor()
	query = 'INSERT INTO Content (username, content_name, public) VALUES(%s, %s, %s)'
	cursor.execute(query, (session['username'], "ImageContent", False))

	query = 'INSERT INTO ImageContent VALUES(LAST_INSERT_ID(), %s)'
	cursor.execute(query, (url))

	# content id, group name, group admin
	query = 'INSERT INTO Share VALUES(LAST_INSERT_ID(), %s, %s)'

	cursor.execute(query, session['groupSelected'])

	query = 'SELECT * FROM Share WHERE id=LAST_INSERT_ID()'
	cursor.execute(query)

	data = cursor.fetchone()

	# commit changes and close connetion
	conn.commit()
	cursor.close()

	return redirect(url_for('content_blueprint.messages') +
                 '?groupSelected=' + session['groupSelected'][0] +
                 '&username_creator=' + session['groupSelected'][1]
                 )

@content_blueprint.route('/comment', methods=['POST'])
def comment():
	content_id 		= request.form['ContentID']
	username   		= request.form['commenter_name']
	comment_text  	= request.form['comment_text']


	conn.commit()

	cursor = conn.cursor()
	query = 'INSERT INTO Comment (id, username, comment_text) VALUES(%s, %s, %s)'
	cursor.execute(query, (content_id, username, comment_text))

	conn.commit()


	return redirect(url_for('content_blueprint.messages') +
                 '?groupSelected=' + session['groupSelected'][0] +
                 '&username_creator=' + session['groupSelected'][1]
                 )






@content_blueprint.route('/home/friendgroups/messages', methods=['GET', 'POST'])
def messages():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		friendGroup = (request.args.get("groupSelected"),
		               request.args.get("username_creator"))

		session['groupSelected'] = friendGroup
		username = session['username']

		messages = getMessages()

		return render_template('messages.html', messages=messages)


@content_blueprint.route('/home/friendgroups/getMessages')
def getMessages():
	cursor = conn.cursor()

	query = "SELECT Content.timest,											\
						Content.id as ContentID,							\
						Share.group_name,									\
				        Share.username as group_admin,						\
				        Content.content_name,								\
				        TextContent.text_content,							\
	                    ImageContent.url,									\
				        Content.username as ContentOwner,					\
				        Content.public										\
					FROM Share 												\
					JOIN Content ON Content.id = Share.id					\
				    LEFT JOIN TextContent on Content.id = TextContent.id	\
	                LEFT JOIN ImageContent on Content.id = ImageContent.id	\
				    WHERE group_name = %s  AND Share.username = %s  		\
				    ORDER BY Content.id DESC								"      

	cursor.execute(query, session['groupSelected'])
	messages = cursor.fetchall()


	comments = {}
	query = "SELECT * FROM Comment WHERE id=%s"
	for i, _ in enumerate(messages):
		if messages[i]['url'] != None:
			messages[i]['url'] = urllib.parse.unquote( messages[i]['url'] )

		cursor.execute(query, messages[i]['ContentID'])
		comments[ messages[i]['ContentID'] ] = cursor.fetchall()

	cursor.close()

	return render_template('getMessages.html', contents=messages, comments=comments)
