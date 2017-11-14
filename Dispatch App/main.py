from flask import Flask, request, render_template
from flask import request
import pymysql.cursors

app = Flask(__name__)

#Configure MySQL
#conn = pymysql.connect(host='localhost',
#                       user='root',
#                       password='root',
#                       db='meetup3',
#                       charset='utf8mb4',
#                       cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/loginAuth')
def loginAuth():
    return "Welcome Home!"

@app.route('/register')
def register(): 
    return render_template('register.html')

@app.route('/registerAuth')
def registerAuth():
    return "Welcome Home!"

app.run()

