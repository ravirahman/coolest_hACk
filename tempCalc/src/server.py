from flask import request, jsonify
from flask_api import FlaskAPI
import datetime
from iso import get_cost_proj
from flask_cors import CORS
from eqs import main, calc_naive, calc_temp
from benchmark import calculate_eff
from climate import get_temps

app = FlaskAPI(__name__)
cors = CORS(app)


TOTAL_COUNT = 24


@app.route("/temp", methods=['POST'])
def get_temp():
  global TOTAL_COUNT

  alpha = float(request.data.get('alpha'))
  beta = float(request.data.get('beta'))
  room_temp = float(request.data.get('current'))
  min_temp = float(request.data.get('min'))
  max_temp = float(request.data.get('max'))
  env_temps = get_temps(TOTAL_COUNT)

  dt = datetime.datetime.now()
  costs = get_cost_proj(TOTAL_COUNT, int(dt.strftime("%s")))
  print(costs)

  ac_temps = [float(x) for x in main(alpha, beta, env_temps, room_temp,
              min_temp, max_temp, costs)[0]['x']]
  print(ac_temps)
  print(calc_naive(alpha, beta, env_temps[0], room_temp, min_temp, max_temp))

  eng, cost = calculate_eff(alpha, beta, room_temp, min_temp, max_temp,
                            env_temps, costs, ac_temps, TOTAL_COUNT)

  expected_next_t = calc_temp(alpha, beta, ac_temps[0], env_temps[0],
                              room_temp, 15)

  return jsonify({'response': ac_temps[0], 'en_perc': eng, 'cost_perc': cost,
                  'expected': expected_next_t})


if __name__ == "__main__":
  app.run(host='0.0.0.0')

