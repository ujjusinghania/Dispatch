from flask import session
import hashlib

import sys
if sys.version_info[0] >= 3:
	import urllib.parse
else:
	import urllib

def md5(password):
	# encode and hash password
	m = hashlib.md5()
	password = password.encode('utf-8')
	m.update(password)
	password_digest = m.hexdigest()
	return password_digest


def checkSess():
	return (session['username'] == "" and session['fname'] == "" and session['lname'] == "" and session['color'] == "")


# def checkSess():
# 	return (session['username'] == "" and session['fname'] == "" and session['lname'] == "")

def unquote(messages):
	for i, _ in enumerate(messages):
		if messages[i].get('url')   != None:
			messages[i]['url'] = urllib.parse.unquote( messages[i].get('url') )

		if messages[i].get('img_url')   != None:
			messages[i]['img_url'] = urllib.parse.unquote( messages[i].get('img_url') )

		if messages[i].get('video_url') != None:
			messages[i]['video_url'] = urllib.parse.unquote( messages[i].get('video_url') )

		if messages[i].get('audio_url') != None:
			messages[i]['audio_url'] = urllib.parse.unquote( messages[i].get('audio_url') )
	return messages