from flask import Flask, render_template

app = Flask(__name__)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/account/orders")
def orders():
    return render_template('order_history.html')

@app.route("/account/settings")
def settings():
    return render_template('account_settings.html', data={"name":"Bailey Wimer"})

@app.route("/catalog")
def catalog():
    return render_template('catalog.html', items=[{"name": "Test", "price": 300}, {"name": "Kent Shirt", "price": 27.99}, {"name": "Hat", "price": 10.95}, {"name": "Bill Reed", "price": 100000.00}])

@app.route("/catalog/item")
def item():
    return render_template('item.html')

@app.route("/cart")
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run()