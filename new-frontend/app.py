from flask import Flask, render_template, request, send_file, make_response, redirect
import requests
import json
import os

app = Flask(__name__)

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
          'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


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
        resp.set_cookie('UserID', str(data['customer']))
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
    resp.set_cookie('UserID', str(customer['customer']))
    return resp


@app.route("/account/orders")
def orders():
    customerID = request.cookies.get('UserID')
    if customerID == None:
        return redirect('/login')
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
    return render_template('account_settings.html', customer=customer, states=states)


@app.route('/account/update')
def update():
    customerID = request.cookies.get('UserID')
    if customerID == None:
        return redirect('/login')
    user = {
        "customer": str(customerID),
        "email": request.args.get('email'),
        "password": request.args.get('password'),
        "first_name": request.args.get('fname'),
        "middle_name": request.args.get('mname'),
        "last_name": request.args.get('lname'),
        "phone_number": request.args.get('phone'),
    }

    shipping = {
        "customer": customerID,
        "type": "shipping",
        "street": request.args.get('s_addr'),
        "city": request.args.get('s_city'),
        "state": request.args.get('s_state'),
        "zip": request.args.get('s_zip'),
    }

    billing = {
        "customer": customerID,
        "type": "billing",
        "street": request.args.get('b_addr'),
        "city": request.args.get('b_city'),
        "state": request.args.get('b_state'),
        "zip": request.args.get('b_zip')
    }
    print(billing)
    print(shipping)
    print(requests.post("http://localhost:3000/address/edit", data=shipping).text)
    print(requests.post("http://localhost:3000/address/edit", data=billing).text)
    print(requests.post("http://localhost:3000/customer/edit", data=user).text)
    return redirect('/account/settings')


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
    customerID = request.cookies.get('UserID')
    if customerID == None:
        return redirect('/login')
    selected_variant = request.args.get('variant_id', type=int)
    item_id = request.args.get('item_id')
    r = requests.get("http://localhost:3000/catalog/get",
                     data={"customer": 1, 'item': item_id, 'variant': selected_variant})
    item_info = json.loads(r.text)
    return render_template('item.html', item=item_info, selected_variant=selected_variant)


@app.route("/catalog/item/add")
def addToCart():
    customerID = request.cookies.get('UserID')
    if customerID == None:
        return redirect('/login')
    selected_variant = request.args.get('variant', type=int)
    item_id = request.args.get('item', type=int)
    quantity = request.args.get('quantity', type=int)
    requests.post('http://localhost:3000/cart/add', data={
        "customer": customerID, "item": item_id, "variant": selected_variant, "quantity": quantity})
    return redirect('/cart')


@ app.route("/cart")
def cart():
    customerID = request.cookies.get('UserID')
    if customerID == None:
        return redirect('/login')
    r = requests.get("http://localhost:3000/cart/info",
                     data={"customer": customerID})
    cart_info = json.loads(r.text)
    cart_info['weight'] = round(cart_info['weight'], 2)
    r = requests.get("http://localhost:3000/cart/list",
                     data={"customer": customerID})
    cart = json.loads(r.text)["items"]
    return render_template('cart.html', cart=cart, cart_info=cart_info)


@ app.route("/catalog/item/image")
def image():
    data = {'image': request.args.get("image_id")}
    r = requests.get("http://localhost:3000/image/get", data=data)

    if not r.ok:
        return send_file("./images/noImage.png")

    # if not os.path.exists("./images"):
    #     os.mkdir(f'./images/')
    # with open(f'./images/{request.args.get("image_id")}.jpg', 'wb') as f:
    #     f.write(r.content)

    # TODO: i don't actually know if this is the right way. but it works.
    resp = make_response(r.content, 200)
    resp.headers['Content-Type'] = r.headers['Content-Type']
    resp.headers['Content-Length'] = r.headers['Content-Length']

    return resp


if __name__ == '__main__':
    app.run(debug=True)
