const express = require('express')
const bodyParser = require('body-parser')
const axios = require('axios')
const getPixels = require("get-pixels")
const schedule = require('node-schedule');

var app = express()
const PORT = process.env.PORT || 3000;
const ndarray = require("ndarray")

app.use(bodyParser.json())

/******** THERMO SENSOR ********/

// IR response

app.post('/node/thermo', (req,res) => {
    var img = req.body.img
    var total = 0
    var mean = 0
    var length = img.length
    var width = img[0].length
    for (var i = 0; i < length; i++){
        for (var j = 0; j < width; j++){
            total += img[i][j]
        }
    }

    mean = total/(length * width)

})

// POST: 2D sensor data ---> Process to output ---> 0: No user in room, 1: User active in room, 2: User in active in room
// ---> Call Django ML framework ---> Get optimal setting ---> Send to client

/******** MOBILE APP ********/

// GET: Client will make this call every 30 secs to get optimal temperature

app.post('/node/temp', (req, res) => {
    var request = {
        alpha: 0.05,
        beta: 0.3,
        room_temp: req.body.room_temp,
        min_temp: req.body.min_temp,
        max_temp: req.body.max_temp,
    }

    axios.post('/flask/temp', request)
        .then((response) => {
            var temps = response.temps
            // var metadata = response.body.metadata
            res.status(200).send({
                temps,
                metadata
            })
        })
    })

app.listen(PORT)
console.log("Started backend server on port", PORT)
