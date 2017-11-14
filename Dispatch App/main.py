from flask import Flask, request, render_template
from flask import request
app = Flask(__name__)

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

