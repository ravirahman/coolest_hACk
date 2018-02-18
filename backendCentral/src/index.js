const express = require('express')
const bodyParser = require('body-parser')
const axios = require('axios')
const getPixels = require("get-pixels")
const schedule = require('node-schedule');
const request = require('request');
const async = require('async');

var app = express()
const PORT = process.env.PORT || 5000;
const ndarray = require("ndarray")
const cors = require('cors');

app.use(bodyParser.json())

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

app.post('/setAC', (req, res) => {
  //turn on motor
  
  async.parallel([
    (cb) => {
      var speed = req.body.speed;

      var options = {
        method: 'POST',
        url: 'https://api.particle.io/v1/devices/1f0025001247343438323536/motor',
        headers:
        {
          authorization: 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e',
          'content-type': 'application/x-www-form-urlencoded'
        },
        form: { arg: speed }
      };

      request(options, function (error, response, body) {
        if (error) {
          return cb(error);
        }
        return cb(null, body);
      });
    },
    (cb) => {
      var options = {
        method: 'GET',
        url: 'https://api.particle.io/v1/devices/1f0025001247343438323536/temperature',
        headers:
        {
          authorization: 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e',
          'content-type': 'application/x-www-form-urlencoded'
        },
        form: {}
      };

      request(options, function (error, response, body) {
        if (error) {
          return cb(error);
        }

        const temperature = body.result; //in celcius
        var options = {
          method: 'POST',
          url: 'https://api.particle.io/v1/devices/1f0025001247343438323536/leds_on',
          headers:
          {
            authorization: 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e',
            'content-type': 'application/x-www-form-urlencoded'
          },
          form: { arg: '12345' }
        };

        request(options, function (error, response, body) {
          if (error) {
            return cb(error);
          }
          return cb();
        });
      });
    }
  ], (err, data) => {
    if (err) {
      console.error("Error with setAc", err);
      return res.status(500).send(err);
    }
    return res.send("SUCCESS");
  });
});

app.get('/thermo', (req, res) => {
  async.parallel([
    (cb) => {
      axios({
        url: (PARTICLE + 'top_infra'),
        method: 'get',
        headers: {
          'content-type': 'application/x-www-form-urlencoded',
          'authorization': 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e'
        }
      }).then((res0) => {
        return cb(null, res0.data.result);
        }).catch((err) => cb(err));
    },
    (cb) => {
      axios({
        url: (PARTICLE + 'middle_infra'),
        method: 'get',
        headers: {
          'content-type': 'application/x-www-form-urlencoded',
          'authorization': 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e'
        }
      }).then((res1) => {
        return cb(null, res1.data.result);
      }).catch((err) => cb(err));
    },
    (cb) => {
      axios({
        url: (PARTICLE + 'bottom_infra'),
        method: 'get',
        headers: {
          'content-type': 'application/x-www-form-urlencoded',
          'authorization': 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e'
        }
      }).then((res1) => {
        return cb(null, res1.data.result);
        }).catch((err) => cb(err));
    },
    (cb) => {
      axios({
        url: (LED + 'fan'),
        method: 'get',
        headers: {
          'content-type': 'application/x-www-form-urlencoded',
          'authorization': 'Bearer 2648e0d867f1f3ea045707dde1e98aede2d3d32e'
        }
      }).then((res0) => {
        return cb(null, res0.data.result);
        }).catch((err) => cb(err));
    }
  ], (err, data) => {
    if (err) {
      return res.status(500).send(err);
    }
    var top = data[0];
    var mid = data[1];
    var bottom = data[2];
    var fan = data[3]
    /*if (res2.data.result > 1.1 * res0.data.result) {
      fan = 1
      fanGlobal = 1
      console.log("FAN ON");
    }*/

    var temps = { top, mid, bottom }
    var mean = (top + mid + bottom) / 3
    console.log(temps, mean);
    var sigmoid = { top: sig(temps.top, mean), mid: sig(temps.mid, mean), bottom: sig(temps.bottom, mean) }
    res.status(200).send({ fan, sigTop: sigmoid.top, sigMid: sigmoid.mid, sigBottom: sigmoid.bottom })
  });
});

app.listen(PORT)
console.log("Started backend server on port", PORT)
