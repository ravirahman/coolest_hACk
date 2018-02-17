from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
from eqs import main
from .logger import api_logger

app = FlaskAPI(__name__)
cors = CORS(app)


@app.route("/temp", methods=['POST'])
def get_temp():
	alpha = float(request.data.get('alpha'))
	beta = float(request.data.get('beta'))
	room_temp = float(request.data.get('current'))
	min_temp = float(request.data.get('min'))
	max_temp = float(request.data.get('max'))
  env_temps = GET_ENV_FORECASTS()
  costs = GET_COST_FORECASTS()
  
  temps = main(alpha, beta, env_temps, room_temp, min_temp, max_temp, costs)[0]['x']
	return jsonify({'response': temps})

if __name__ == "__main__":
	api_logger.info('Starting deployment API on 0.0.0.0...')
	app.run(host='0.0.0.0')

