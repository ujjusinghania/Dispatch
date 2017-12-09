from flask import Flask, request, render_template, session, url_for, redirect
from flask import request
from flask import Blueprint
import pymysql.cursors
import hashlib
import helpers

media_blueprint = Blueprint('media_blueprint',__name__)

# this is for pulling the port and database password from environment variables
import os
import sys
if sys.version_info[0] >= 3:
	import urllib.parse
else:
	import urllib

# Configure MySQL
conn = pymysql.connect(host='localhost',
                      port= int(os.environ['DB_PORT']), #get the port from an env var
                      user='root',
                      password=os.environ['DB_PASS'], #get the pswd from an env var
                      db='dispatch',
                      charset='latin1',
                      cursorclass=pymysql.cursors.DictCursor)

# Functions pertaining to content
@media_blueprint.route('/addPublicContent', methods=['GET', 'POST'])
def addPublicContent():
	content 		= request.form['input_text']
	content_type 	= request.form['content_type']
	is_public 		= request.form.get('is_public') != None
	conn.commit()


	cursor = conn.cursor()

	# insert base content object
	query = 'INSERT INTO Content (username, content_name, public) VALUES(%s, %s, %s)'
	cursor.execute(query, (session['username'], content_type, '1'))
	
	# insert spacific type
	query = 'INSERT INTO '+content_type+' VALUES(LAST_INSERT_ID(), %s)'
	cursor.execute(query, content)

	# content id, group name, group admin
	#query = 'INSERT INTO Share VALUES(LAST_INSERT_ID(), %s, %s)'
	#cursor.execute(query, session['groupSelected'])
	
	# query = 'SELECT * FROM Share WHERE id=LAST_INSERT_ID()'
	# cursor.execute(query)
	
	# data = cursor.fetchone()
	cursor.close()
	conn.commit()

	return redirect(url_for('.medialibrary'))		

@media_blueprint.route('/PublicComment', methods=['POST'])
def PublicComment():
	content_id 		= request.form['ContentID']
	username   		= request.form['commenter_name']
	comment_text  	= request.form['comment_text']


	conn.commit()

	cursor = conn.cursor()
	query = 'INSERT INTO Comment (id, username, comment_text) VALUES(%s, %s, %s)'
	cursor.execute(query, (content_id, username, comment_text))

	conn.commit()


	return redirect(url_for('.medialibrary'))
	
@media_blueprint.route('/home/medialibrary', methods=['GET'])
def medialibrary():
	if (helpers.checkSess()):
		return redirect(url_for('login'))
	else:
		cursor = conn.cursor()
		
		#Query gets all the content that the user can view (public content and content in groups user is part of)
		query = "SELECT Content.timest,										\
						Content.id as ContentID,							\
						Share.group_name,									\
				        Share.username as group_admin,						\
				        Content.content_name,								\
				        TextContent.text_content,							\
	                    ImageContent.url as img_url,						\
						AudioContent.url as audio_url,						\
						VideoContent.url as video_url,						\
				        Content.username as ContentOwner,					\
				        Content.public										\
					FROM Share 												\
					JOIN Content ON Content.id = Share.id					\
				    LEFT JOIN TextContent on Content.id = TextContent.id	\
	                LEFT JOIN ImageContent on Content.id = ImageContent.id	\
					LEFT JOIN AudioContent ON Content.id = AudioContent.id 	\
					LEFT JOIN VideoContent ON Content.id = VideoContent.id 		\
				    WHERE Content.public='1' OR Content.id IN								  		\
				    (SELECT id FROM Share WHERE (group_name, username) IN	\
				    (SELECT group_name, username_creator FROM Member WHERE username = %s OR username_creator = %s)) \
					ORDER BY Content.id ASC								"      
					
		cursor.execute(query, (session['username'], session['username']))
		messages = cursor.fetchall()


		comments = {}
		query = "SELECT * FROM Comment WHERE id= %s"
		for i, _ in enumerate(messages):
			print(messages[i])
			if messages[i]['img_url'] != None:
				messages[i]['img_url'] = urllib.parse.unquote( messages[i]['img_url'] )
			elif messages[i]['audio_url'] != None:
				messages[i]['audio_url'] = urllib.parse.unquote( messages[i]['audio_url'] )
			if messages[i]['video_url'] != None:
				messages[i]['video_url'] = urllib.parse.unquote( messages[i]['video_url'] )

			cursor.execute(query, messages[i]['ContentID'])
			comments[ messages[i]['ContentID'] ] = cursor.fetchall()

		cursor.close()

		print(messages)

		return render_template("media.html", contents=messages, comments=comments)
