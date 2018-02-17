from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
from eqs import main
from climate import get_temps

app = FlaskAPI(__name__)
cors = CORS(app)


@app.route("/temp", methods=['POST'])
def get_temp():
  alpha = float(request.data.get('alpha'))
  beta = float(request.data.get('beta'))
  room_temp = float(request.data.get('current'))
  min_temp = float(request.data.get('min'))
  max_temp = float(request.data.get('max'))
  env_temps = get_temps()
  costs = [1,1,1,1]
  
  temps = [float(x) for x in main(alpha, beta, env_temps, room_temp, min_temp, max_temp, costs)[0]['x']]
  return jsonify({'response': temps})

if __name__ == "__main__":
  app.run(host='0.0.0.0')

