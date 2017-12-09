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
	caption			= request.form['caption_box']

	if (content == ""):
		return redirect(url_for('.medialibrary'))

	cursor = conn.cursor()

	# insert base content object
	query = 'INSERT INTO Content (username, content_name, public, caption) VALUES(%s, %s, %s, %s)'
	cursor.execute(query, (session['username'], content_type, '1', caption))

	# insert spacific type
	query = 'INSERT INTO '+content_type+' VALUES(LAST_INSERT_ID(), %s)'
	cursor.execute(query, content)

	cursor.close()
	conn.commit()

	return redirect(url_for('.medialibrary'))		

@media_blueprint.route('/PublicComment', methods=['POST'])
def PublicComment():
	content_id 		= request.form['ContentID']
	username   		= request.form['commenter_name']
	comment_text  	= request.form['comment_text']
	
	if (comment_text == ""):
		return redirect(url_for('.medialibrary'))
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
		query = "(SELECT														\
					Content.timest,												\
				    Content.id AS ContentID,									\
				    Content.content_name,										\
				    TextContent.text_content,									\
				    ImageContent.url AS img_url,								\
				    AudioContent.url AS audio_url,								\
				    VideoContent.url AS video_url,								\
				    Content.username AS ContentOwner,							\
				    Content.public 												\
				FROM SHARE														\
				JOIN Content ON Content.id = SHARE.id							\
				LEFT JOIN TextContent ON Content.id = TextContent.id 			\
				LEFT JOIN ImageContent ON Content.id = ImageContent.id 			\
				LEFT JOIN AudioContent ON Content.id = AudioContent.id 			\
				LEFT JOIN VideoContent ON Content.id = VideoContent.id			\
				WHERE															\
				    Content.id IN 											 	\
				    (SELECT id													\
				     FROM Share													\
				     WHERE (group_name, username) IN							\
				     	(SELECT group_name, username_creator 					\
				         FROM member											\
				         WHERE username = %s OR username_creator = %s))			\
						 ORDER BY Content.id ASC)								\
				UNION 															\
				(SELECT Content.timest,											\
				    Content.id AS ContentID,									\
				    Content.content_name,										\
				    TextContent.text_content,									\
				    ImageContent.url AS img_url,								\
				    AudioContent.url AS audio_url,								\
				    VideoContent.url AS video_url,								\
				    Content.username AS ContentOwner,							\
				    Content.public 												\
				FROM Content 													\
				LEFT JOIN TextContent ON Content.id = TextContent.id 			\
				LEFT JOIN ImageContent ON Content.id = ImageContent.id 			\
				LEFT JOIN AudioContent ON Content.id = AudioContent.id 			\
				LEFT JOIN VideoContent ON Content.id = VideoContent.id 			\
							WHERE Content.public = 1)						    "

		cursor.execute(query, (session['username'], session['username'])) 
		messages = cursor.fetchall() 

		query = ""

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
