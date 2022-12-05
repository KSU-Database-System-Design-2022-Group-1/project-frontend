from flask import Flask, render_template, request, send_file, make_response
import requests
import json
import os

app = Flask(__name__)


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/login/go", methods= ['POST'])
def loginAction():
    user = request.form['email']
    password = request.form['password']
    r = requests.get("http://localhost:3000/customer/signin", data={"email": user, "password": password})
    resp = make_response()
    

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
    r = requests.get("http://localhost:3000/customer/get", data={"customer": 1})
    customer = json.loads(r.text)
    return render_template('account_settings.html', customer=customer)


@app.route("/")
@app.route("/catalog")
def catalog():
    search_data = {
        "name": request.args.get('search'),
        "color": request.args.get('color'),
        "size": request.args.get('size'),
        "minprice": request.args.get('price_min'),
        "maxprice": request.args.get('price_max'),
        "category": request.args.get('category')
    }
    r = requests.get("http://localhost:3000/catalog/search", data=search_data)
    items = json.loads(r.text)["items"]
    return render_template('catalog.html', items=items)


@app.route("/catalog/item")
def item():
    selected_variant = request.args.get('variant_id')
    item_id = request.args.get('item_id')
    r = requests.get("http://localhost:3000/catalog/get", data={"customer": 1, 'item': item_id, 'variant': selected_variant})
    item_info = json.loads(r.text)
    return render_template('item.html', item=item_info, selected_variant=selected_variant)


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
