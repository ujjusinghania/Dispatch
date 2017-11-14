from flask import Flask, request, render_template
from flask import request
import pymysql.cursors

app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='meetup3',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def homepage():
    return render_template('index.html');

@app.route('/hello')
def hello():
    return '<h1>"Hello"</h1><a = href "/goodbye">goodbye</a>'

@app.route('/goodbye')
def goodbye():
    return "Welcome Home!"

@app.route('/pizza')
def pizza():
    topping = "Chicken"
    toppings = ["pepperoni","pineapple", "sausage", "Mushrooms"]
    return render_template("pizza.html", topping = topping)

@app.route('/pizza/create', methods = ["POST"])
def pizza_create():
    return request.form['crust']

app.run()

