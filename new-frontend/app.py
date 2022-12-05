from flask import Flask, render_template, request, send_file
import requests
import json
import os

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
    return render_template('account_settings.html', customer={"first_name": "Bailey", "last_name": "Wimer", "email": "bwimer3@kent.edu", "shipping_address": "123 Kent Rd. NE", "shipping_city": "Kent", "shipping_zip": "12345", "billing_address": "123 Kent Rd. NE", "billing_city": "Kent", "billing_zip": "12345", "phone_number": "5555555555"})


@app.route("/")
@app.route("/catalog")
def catalog():
    search = request.args.get('search')
    color = request.args.get('color')
    size = request.args.get('size')
    price_min = request.args.get('price_min')
    price_max = request.args.get('price_max')
    category = request.args.get('category')
    return render_template('catalog.html', items=[{"item_id": 1, "name": "Test", "price": 300}, {"item_id": 2, "name": "Kent Shirt", "price": 27.99}, {"item_id": 3, "name": "Hat", "price": 10.95}, {"item_id": 4, "name": "Bill Reed", "price": 100000.00}])


@app.route("/catalog/item")
def item():
    selected_variant = int(request.args.get('variant_id'))
    return render_template('item.html', item={"item_id": 1, "name": "Test", "description": "This is a test and only a test", "category": "Shirt", "price": 52.95, "stock": 22, "variants": [{"variant_id": 1, "size": "M", "color": "Blue", "price": "15.99"}, {"variant_id": 2, "size": "L", "color": "Blue", "price": "12.55"}, {"variant_id": 3, "size": "XL", "color": "Blue", "price": "20.00"}, {"variant_id": 4, "size": "XL", "color": "Red", "price": "40.99"}]}, selected_variant=selected_variant)


@ app.route("/cart")
def cart():
    r = requests.get("http://localhost:3000/cart/info", data={"customer": 1})
    cart_info = json.loads(r.text)
    cart_info['weight'] = round(cart_info['weight'], 2)
    r = requests.get("http://localhost:3000/cart/list", data={"customer": 1})
    cart = json.loads(r.text)["items"]
    return render_template('cart.html', cart=cart, cart_info=cart_info)


@ app.route("/catalog/item/image")
def image():
    r = requests.get(
        "https://d33wubrfki0l68.cloudfront.net/13d099d0ba920a02c9e37e336cb35c7939a2c7d3/0f08e/images/ghost/2022-06-13-5-image-apis-you-can-use-for-your-next-project-in-2022/6.jpeg", stream=True)
    try:
        os.mkdir(f'./images/{request.args.get("item_id")}/')
    except:
        print("dir already exists")
    with open(f'./images/{request.args.get("item_id")}/{request.args.get("variant_id")}.jpg', 'wb') as f:
        f.write(r.content)
    return send_file(f'./images/{request.args.get("item_id")}/{request.args.get("variant_id")}.jpg', mimetype="image/jpeg")


if __name__ == '__main__':
    app.run(debug=True)
