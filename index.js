var express = require('express');
var app = express();

const port = 3000

app.use(express.static(__dirname + '/public'));

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/pages/home.html')
});


app.listen(port);