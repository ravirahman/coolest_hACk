from flask import request, jsonify
from flask_api import FlaskAPI
import datetime
from iso import get_cost_proj
from flask_cors import CORS
from eqs import main, calc_naive, calc_temp
from climate import get_temps

app = FlaskAPI(__name__)
cors = CORS(app)


total_cost = 0
total_pot_cost = 0

total_en = 0
total_pot_en = 0


@app.route("/temp", methods=['POST'])
def get_temp():
  global total_cost
  global total_pot_cost
  global total_en
  global total_pot_en

  alpha = float(request.data.get('alpha'))
  beta = float(request.data.get('beta'))
  room_temp = float(request.data.get('current'))
  min_temp = float(request.data.get('min'))
  max_temp = float(request.data.get('max'))
  env_temps = get_temps()

  dt = datetime.datetime.now()
  costs = get_cost_proj(int(dt.strftime("%s")))
  print(costs)
  
  temps = [float(x) for x in main(alpha, beta, env_temps, room_temp, min_temp, max_temp, costs)[0]['x']]

  print(calc_naive(alpha, beta, env_temps[0], room_temp, min_temp, max_temp))
  print(temps)

  total_cost += costs[0] * abs(temps[0] - env_temps[0])
  total_pot_cost += costs[0] * abs(calc_naive(alpha, beta, env_temps[0], room_temp, min_temp, max_temp) - env_temps[0])
  total_en += abs(temps[0] - env_temps[0])
  total_pot_en += abs(calc_naive(alpha, beta, env_temps[0], room_temp, min_temp, max_temp) - env_temps[0])

  eng_saved = 100 * (total_pot_en / total_en) / total_en
  cost_saved = 100 * (total_pot_cost / total_cost) / total_cost

  expected_next_t = calc_temp(alpha, beta, temps[0], env_temps[0], room_temp, 15)

  return jsonify({'response': temps[0], 'en_perc': eng_saved, 'cost_perc': cost_saved, 'expected': expected_next_t})

if __name__ == "__main__":
  app.run(host='0.0.0.0')

