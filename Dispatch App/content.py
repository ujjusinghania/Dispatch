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

# Functions pertaining to content
@content_blueprint.route('/addContent', methods=['GET', 'POST'])
def addContent():
	content 		= request.form['input_text']
	content_type 	= request.form['content_type']
	caption			= request.form['caption_box']
	is_public 		= request.form.get('is_public') != None
	conn.commit()

	if (content == ""):
		return redirect(url_for('content_blueprint.messages') +
                 '?groupSelected=' + session['groupSelected'][0] +
                 '&username_creator=' + session['groupSelected'][1]
                )

	cursor = conn.cursor()

	# insert base content object
	query = 'INSERT INTO Content (username, content_name, public, caption) VALUES(%s, %s, %s, %s)'
	cursor.execute(query, (session['username'], content_type, is_public, caption))
	
	# insert spacific type
	query = 'INSERT INTO '+content_type+' VALUES(LAST_INSERT_ID(), %s)'
	cursor.execute(query, content)

	# content id, group name, group admin
	query = 'INSERT INTO Share VALUES(LAST_INSERT_ID(), %s, %s)'
	cursor.execute(query, session['groupSelected'])
	
	# query = 'SELECT * FROM Share WHERE id=LAST_INSERT_ID()'
	# cursor.execute(query)
	
	# data = cursor.fetchone()
	cursor.close()
	conn.commit()
	
	
	return redirect(url_for('content_blueprint.messages') +
                 '?groupSelected=' + session['groupSelected'][0] +
                 '&username_creator=' + session['groupSelected'][1]
                )

@content_blueprint.route('/addContentToProfile',methods=['POST'])
def addContentToProfile():
	content 		= request.form['input_text']
	content_type 	= request.form['content_type']
	is_public 		= request.form.get('is_public') != None
	conn.commit()

	cursor=conn.cursor()

    # insert base content object
	query = 'INSERT INTO Content (username, content_name, public) VALUES(%s, %s, %s)'
	cursor.execute(query, (session['username'], content_type, is_public))
	
	# insert spacific type
	query = 'INSERT INTO '+content_type+' VALUES(LAST_INSERT_ID(), %s)'
	cursor.execute(query, content)

	query = 'UPDATE person SET profilePic = LAST_INSERT_ID() WHERE username = %s'
	cursor.execute(query,session['username'])

	conn.commit()
	cursor.close()


	return redirect(url_for('profile'))

@content_blueprint.route('/comment', methods=['POST'])
def comment():
	content_id 		= request.form['ContentID']
	username   		= request.form['commenter_name']
	comment_text  	= request.form['comment_text']

	if (comment_text == ""):
		return redirect(url_for('content_blueprint.messages') +
                 '?groupSelected=' + session['groupSelected'][0] +
                 '&username_creator=' + session['groupSelected'][1]
                )

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

@content_blueprint.route('/addFavorite')
def addFavorite():

	conn.commit()
	cursor = conn.cursor()

	query = "INSERT INTO Favorite (id, username) VALUES(%s, %s);"

	cursor.execute(query, (request.args.get("content_id"), session['username']))

	cursor.close()
	conn.commit()	


	return redirect(url_for('content_blueprint.messages') +
                 '?groupSelected=' + session['groupSelected'][0] +
                 '&username_creator=' + session['groupSelected'][1]
                 )


@content_blueprint.route('/addTag',methods=['POST'])
def addTag():
	content_id = request.args.get('content_id')
	username = request.form['taggee_name']

	conn.commit()

	cursor = conn.cursor()
	query = 'INSERT INTO tag (id,username_tagger,username_taggee,status) VALUES (%s,%s,%s, False)'
	cursor.execute(query,(content_id,username,session['username']))

	conn.commit()
	return redirect(url_for('.medialibrary'))


@content_blueprint.route('/home/favorites')
def favorites():
	cursor = conn.cursor()

	query = "SELECT timest,										\
		Favorite.id as ContentID,								\
        Content.username as ContentOwner,						\
        Content.caption,										\
        Content.content_name,									\
        TextContent.text_content,								\
		ImageContent.url as img_url,							\
		VideoContent.url as video_url,							\
		AudioContent.url as audio_url,							\
		Content.username as ContentOwner,						\
        Content.public											\
        public 													\
	FROM Favorite 												\
	JOIN Content ON Content.id = Favorite.id 					\
    LEFT JOIN TextContent  ON Content.id = TextContent.id 		\
    LEFT JOIN AudioContent ON Content.id = AudioContent.id 		\
    LEFT JOIN VideoContent ON Content.id = VideoContent.id 		\
    LEFT JOIN ImageContent ON Content.id = ImageContent.id 		\
    WHERE Favorite.username = %s; 								"

	cursor.execute(query, session['username'])
	favs = cursor.fetchall()
	favs = unquote(favs)


	print(favs)
	# get comments 
	comments = {} #dict for comments 
	query = "SELECT * FROM Comment WHERE id=%s"

	# loop through all the messages and store the comments for each one in a dict
	for i in range(len(favs)):
		cursor.execute(query, favs[i]['ContentID'])
		comments[ favs[i]['ContentID'] ] = cursor.fetchall()

	cursor.close()

	return render_template('favorites.html', contents=favs, comments=comments)



@content_blueprint.route('/home/friendgroups/getMessages')
def getMessages():
	cursor = conn.cursor()

	query = "SELECT Content.timest,											\
						Content.id as ContentID,							\
						Content.caption,									\
						Share.group_name,									\
				        Share.username as group_admin,						\
				        Content.content_name,								\
				        TextContent.text_content,							\
						ImageContent.url as img_url,						\
						VideoContent.url as video_url,						\
						AudioContent.url as audio_url,						\
						Content.username as ContentOwner,					\
				        Content.public										\
					FROM Share 												\
					JOIN Content ON Content.id = Share.id					\
				    LEFT JOIN TextContent  ON Content.id = TextContent.id	\
	                LEFT JOIN ImageContent ON Content.id = ImageContent.id	\
	                LEFT JOIN VideoContent ON Content.id = VideoContent.id	\
	                LEFT JOIN AudioContent ON Content.id = AudioContent.id	\
				    WHERE group_name = %s  AND Share.username = %s  		\
				    ORDER BY Content.id ASC								"      

	cursor.execute(query, session['groupSelected'])
	messages = cursor.fetchall()
	messages = unquote(messages)


	# get comments 
	comments = {} #dict for comments 
	query = "SELECT * FROM Comment WHERE id=%s"

	# loop through all the messages and store the comments for each one in a dict
	for i in range(len(messages)):
		cursor.execute(query, messages[i]['ContentID'])
		comments[ messages[i]['ContentID'] ] = cursor.fetchall()

	cursor.close()

	return render_template('getMessages.html', contents=messages, comments=comments)



def unquote(messages):
	for i, _ in enumerate(messages):
		if messages[i]['img_url']   != None:
			messages[i]['img_url']   = urllib.parse.unquote( messages[i]['img_url'] )

		if messages[i]['video_url'] != None:
			messages[i]['video_url'] = urllib.parse.unquote( messages[i]['video_url'] )

		if messages[i]['audio_url'] != None:
			messages[i]['audio_url'] = urllib.parse.unquote( messages[i]['audio_url'] )
	return messages


