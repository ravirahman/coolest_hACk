const express = require('express')
const bodyParser = require('body-parser')
const axios = require('axios')
const getPixels = require("get-pixels")
const schedule = require('node-schedule');
var FormData = require('form-data');

var app = express()
const PORT = process.env.PORT || 5000;
const ndarray = require("ndarray")
const cors = require('cors');

app.use(bodyParser.json())

var fanGlobal = 0

const PARTICLE = "https://api.particle.io/v1/devices/34005b000e51353532343635/"
const LED = "https://api.particle.io/v1/devices/1f0025001247343438323536/"

app.use(cors({
  credentials: true,
  origin: 'http://localhost:3000'
}));

var userMode = "active"

/******** THERMO SENSOR ********/

// IR response

function sig(x, mean){
    return 1.0/(1+Math.pow(2.718, (-1.0*x+mean)));

}

app.post('/setAC', (req,res) => {
    const config = { headers: {
        'content-type': 'application/x-www-form-urlencoded',
        'authorization': 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e'
        }
    }
    var speed = req.body.speed
    var bodyFormData = new FormData();
    bodyFormData.append('arg', speed);
    axios({
        url: (LED + 'motor'),
        method: 'post',
        config,
        data: bodyFormData
    })
        .then((res0) => {
            console.log(res0.data);
        })

    axios({
        url: (LED + 'temperature'),
        method: 'get',
        headers: {
            'content-type': 'application/x-www-form-urlencoded',
            'authorization': 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e'
        }
        })
        .then((res0) => {
            var temp = res0.data.result
            console.log(temp);
            var fd = new FormData();
            fd.append('arg', "12345");
            axios({
                url: (LED + 'leds_on'),
                method: 'post',
                config,
                data: fd
                })
                .then((res1) => {
                    console.log(res1.status);
                    res.status(200).send("SUCCESS")
                })
        })

})



app.get('/thermo', (req,res) => {
    axios({
        url: (PARTICLE + 'top_infra'),
        method: 'get',
        headers: {
            'content-type': 'application/x-www-form-urlencoded',
            'authorization': 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e'
        }
    })
    .then((res0) => {
        axios({
            url: (PARTICLE + 'middle_infra'),
            method: 'get',
            headers: {
                'content-type': 'application/x-www-form-urlencoded',
                'authorization': 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e'
            }
        })
        .then((res1) => {
            axios({
                url: (PARTICLE + 'bottom_infra'),
                method: 'get',
                headers: {
                    'content-type': 'application/x-www-form-urlencoded',
                    'authorization': 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e'
                }
            })
            .then((res2) => {
                var top = res0.data.result
                var mid = res1.data.result
                var bottom = res2.data.result
                var fan = 0
                if (res2.data.result > 1.1*res0.data.result){
                    fan = 1
                    fanGlobal = 1
                    console.log("FAN ON");
                }

                var temps = {top, mid, bottom}
                var mean =  (res0.data.result + res1.data.result + res2.data.result)/3
                console.log(temps, mean);
                var sigmoid = {top: sig(temps.top, mean), mid: sig(temps.mid, mean), bottom: sig(temps.bottom, mean)}
                res.status(200).send({fan, sigTop: sigmoid.top, sigMid: sigmoid.mid, sigBottom: sigmoid.bottom})
            })
        })
    })
})

app.listen(PORT)
console.log("Started backend server on port", PORT)
