const path = require('path');
const express = require('express')

const app = express()
const port = 3000

let userLoggedIn = false;

app.get('/', (req, res) => {
    if(userLoggedIn)
        res.sendFile(path.join(__dirname, '/pages/home.html'))
    else
        res.redirect('/login')
})

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'pages/login.html'))
    userLoggedIn = true;
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})