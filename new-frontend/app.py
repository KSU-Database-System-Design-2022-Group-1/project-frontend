from flask import Flask, render_template, request, send_file, make_response, redirect
import requests
import json
import os

app = Flask(__name__)


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/login/go", methods=['GET', 'POST'])
def loginAction():
    user = request.args.get('email')
    password = request.args.get('password')
    r = requests.get("http://localhost:3000/customer/signin",
                     data={"email": user, "password": password})
    data = json.loads(r.text)
    if data['valid']:
        resp = make_response(redirect('/catalog'))
        r = requests.get("http://localhost:3000/customer/signin",
                         data={"email": user, "password": password})
        resp.set_cookie('UserID', '1')
        return resp
    else:
        return redirect('/login')


@app.route("/signout", methods=['GET'])
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie('UserID', '', expires=0)
    return resp


@app.route("/register")
def register():
    return render_template('register.html')


@app.route('/register/go')
def registerAction():
    user = {
        "email": request.args.get('email'),
        "password": request.args.get('password'),
        "first_name": request.args.get('fname'),
        "middle_name": request.args.get('mname'),
        "last_name": request.args.get('lname'),
        "phone_number": request.args.get('phone'),
        "shipping_street": request.args.get('s_addr'),
        "shipping_city": request.args.get('s_city'),
        "shipping_state": request.args.get('s_state'),
        "shipping_zip": request.args.get('s_zip'),
        "billing_street": request.args.get('b_addr'),
        "billing_city": request.args.get('b_city'),
        "billing_state": request.args.get('b_state'),
        "billing_zip": request.args.get('b_zip')
    }
    r = requests.post("http://localhost:3000/customer/signup", data=user)
    print(r.text)
    customer = json.loads(r.text)
    resp = make_response(redirect('/catalog'))
    resp.set_cookie('UserID', customer['customer'])
    return resp


@app.route("/account/orders")
def orders():
    r = requests.get("http://localhost:3000/order/list", data={"customer": 1})
    orders = json.loads(r.text)["orders"]
    return render_template('order_history.html', orders=orders)


@app.route("/account/settings")
def settings():
    customerID = request.cookies.get('UserID')
    if customerID == None:
        return redirect('/login')
    r = requests.get("http://localhost:3000/customer/get",
                     data={"customer": customerID})
    customer = json.loads(r.text)
    print(customer)
    return render_template('account_settings.html', customer=customer)


@app.route("/")
@app.route("/catalog")
def catalog():
    customerID = request.cookies.get('UserID')
    if customerID == None:
        return redirect('/login')

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
    selected_variant = request.args.get('variant_id', type=int)
    item_id = request.args.get('item_id')
    r = requests.get("http://localhost:3000/catalog/get",
                     data={"customer": 1, 'item': item_id, 'variant': selected_variant})
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
    data = {'image': request.args.get("image_id")}
    try:
        r = requests.get("http://localhost:3000/image/get", data=data)
    except:
        r = requests.get("http://localhost:3000/image/get", data={'image': 1})
    try:
        os.mkdir(f'./images/')
    except:
        print("dir already exists")
    with open(f'./images/{request.args.get("image_id")}.jpg', 'wb') as f:
        f.write(r.content)
    return send_file(f'./images/{request.args.get("image_id")}.jpg', mimetype="image/jpeg")


if __name__ == '__main__':
    app.run(debug=True)
