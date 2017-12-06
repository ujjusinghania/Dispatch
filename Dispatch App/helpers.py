from flask import session
import hashlib


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

