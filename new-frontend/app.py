from flask import Flask, render_template
import requests
import json

app = Flask(__name__)


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/account/orders")
def orders():
    r = requests.get("http://localhost:3000/order/list", data={"customer": 1})
    orders = json.loads(r.text)["orders"]
    return render_template('order_history.html', orders=orders)


@app.route("/account/settings")
def settings():
    return render_template('account_settings.html', customer={"first_name": "Bailey", "last_name": "Wimer", "email": "bwimer3@kent.edu", "shipping_address": "123 Kent Rd. NE", "shipping_city": "Kent", "shipping_zip": "12345", "billing_address": "123 Kent Rd. NE", "billing_city": "Kent", "billing_zip": "12345"})


@app.route("/")
@app.route("/catalog")
def catalog():
    return render_template('catalog.html', items=[{"name": "Test", "price": 300}, {"name": "Kent Shirt", "price": 27.99}, {"name": "Hat", "price": 10.95}, {"name": "Bill Reed", "price": 100000.00}])


@app.route("/catalog/item")
def item():
    return render_template('item.html', item={"name": "Test", "description": "This is a test and only a test", "category": "Shirt", "price": 52.95, "stock": 22, "variants": [{"size": "M", "color": "Blue"}, {"size": "L", "color": "Blue"}, {"size": "XL", "color": "Blue"}, {"size": "XL", "color": "Red"}]})


@app.route("/cart")
def cart():
    r = requests.get("http://localhost:3000/cart/info", data={"customer": 1})
    cart_info = json.loads(r.text)
    cart_info['weight'] = round(cart_info['weight'], 2)
    r = requests.get("http://localhost:3000/cart/list", data={"customer": 1})
    cart = json.loads(r.text)["items"]
    return render_template('cart.html', cart=cart, cart_info=cart_info)


@app.route("/catalog/item/image")
def image():
    return


if __name__ == '__main__':
    app.run(debug=True)
