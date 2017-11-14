from flask import Flask, request, render_template
from flask import request
import pymysql.cursors

app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='',
                       db='dispatch',
                       charset='latin1',
                       cursorclass=pymysql.cursors.DictCursor)


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

