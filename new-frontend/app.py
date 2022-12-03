from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

# app.secret_key = 'your secret key'

@app.route("/login")
def login():
    # I believe that in order to make the authentication work we need to switch username to "email" and then add
    # request, redirect, and session to the import flask statement. Next, uncomment all of the "if 'loggedin' not
    # in session' statements and the secret key statement. For reference go to l7-3-examples-flask\l7-3\flask-login
    # from the files that he provided from class. I beliece that the session['loggedin'] = True statement and the
    # following statements add the data to the session and can be accessed in the other functions.

    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    #     # Create variables for easy access
    #     username = request.form['username']
    #     password = request.form['password']
    #     # Check if account exists using MySQL
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
    #     # Fetch one record and return result
    #     account = cursor.fetchone()
    #     # If account exists in accounts table in out database
    #     if account:
    #         # Create session data, we can access this data in other routes
    #         session['loggedin'] = True
    #         session['id'] = account['id']
    #         session['username'] = account['username']
    #         # Redirect to home page
    #         return redirect(url_for('home'))

    # Show the login form with message (if any)
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/account/orders")
def orders():
    # if 'loggedin' not in session:
    #     return redirect(url_for('login'))
    # else:
    return render_template('order_history.html')

@app.route("/account/settings")
def settings():
    # if 'loggedin' not in session:
    #     return redirect(url_for('login'))
    # else:
    return render_template('account_settings.html', data={"name":"Bailey Wimer"})

@app.route("/")
@app.route("/catalog")
def catalog():
    # if 'loggedin' not in session:
    #     return redirect(url_for('login'))
    # else:
    return render_template('catalog.html', items=[{"name": "Test", "price": 300}, {"name": "Kent Shirt", "price": 27.99}, {"name": "Hat", "price": 10.95}, {"name": "Bill Reed", "price": 100000.00}])

@app.route("/catalog/item")
def item():
    # if 'loggedin' not in session:
    #     return redirect(url_for('login'))
    # else:
    return render_template('item.html')

@app.route("/cart")
def cart():
    # r = requests.get("http://localhost:3000/cart/info", data={"customer": 1})
    # cart_info = json.loads(r.text)
    # cart_info['price'] = round(cart_info['price'], 2)
    # cart_info['weight'] = round(cart_info['weight'], 2)
    # r = requests.get("http://localhost:3000/cart/list", data={"customer": 1})
    # cart = json.loads(r.text)["item"]
    cart = []
    cart_info = {}
    # if 'loggedin' not in session:
    #     return redirect(url_for('login'))
    # else:
    return render_template('cart.html', cart=cart, cart_info=cart_info)

@app.route("/catalog/item/image")
def image():
    return

if __name__ == '__main__':
    app.run()