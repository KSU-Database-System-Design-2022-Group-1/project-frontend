// CommonJS module import using ES6 syntax
import express from 'express';

var app = express();

const port = 3000;

app.use(express.static(__dirname + '/public'));

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/pages/home.html')
});

app.get('/account', function(req, res) {
    res.sendFile(__dirname + '/pages/account_landing.html')
});

app.get('/account/settings', function(req, res) {
    res.sendFile(__dirname + '/pages/account_settings.html')
});

app.get('/account/orders', function(req, res) {
    res.sendFile(__dirname + '/pages/order_history.html')
});

app.get('/login', function(req, res) {
    res.sendFile(__dirname + '/pages/login.html')
});

app.get('/register', function(req, res) {
    res.sendFile(__dirname + '/pages/register.html')
});

app.get('/catalog', function(req, res) {
    res.sendFile(__dirname + '/pages/catalog.html')
});

app.get('/catalog/item', function(req, res) {
    res.sendFile(__dirname + '/pages/item.html')
});

app.get('/cart', function(req, res) {
    res.sendFile(__dirname + '/pages/cart.html')
});

app.get('/checkout', function(req, res) {
    res.sendFile(__dirname + '/pages/home.html')
});

app.listen(port);
