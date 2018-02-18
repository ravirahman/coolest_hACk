import datetime
from climate import get_temps
from iso import get_cost_proj
from eqs import main, calc_naive, calc_temp


def calculate_eff(alpha, beta, room_temp, min_temp, max_temp,
                  env_temps, costs, ac_temps, TOTAL_COUNT):
  total_pot_en = 0
  total_pot_cost = 0
  history = [room_temp]
  for i in range(TOTAL_COUNT):
    ac_temp = calc_naive(alpha, beta, env_temps[i], history[i],
                         min_temp, max_temp)
    total_pot_en += abs((env_temps[i] - ac_temp))
    total_pot_cost += abs((env_temps[i] - ac_temp)) * costs[i]
    history.append(calc_temp(alpha, beta, ac_temp, env_temps[i],
                             history[i], 15))
  print(total_pot_en)
  print(total_pot_cost)

  # Estimate real
  total_en = 0
  total_cost = 0
  for i in range(TOTAL_COUNT):
    total_en += abs((env_temps[i] - ac_temps[i]))
    total_cost += abs((env_temps[i] - ac_temps[i])) * costs[i]
  print(total_en)
  print(total_cost)

  eng_saved = 100 * abs(total_pot_en - total_en) / total_en
  cost_saved = 100 * abs(total_pot_cost - total_cost) / total_cost
  print("Saved energy %:", eng_saved)
  print("Saved cost %:", cost_saved)

  return eng_saved, cost_saved


if __name__ == "__main__":
  alpha = 0.009
  beta = 0.2
  room_temp = 75
  min_temp = 60
  max_temp = 70
  TOTAL_COUNT = 100
  env_temps = get_temps(TOTAL_COUNT)

  dt = datetime.datetime.now()
  costs = get_cost_proj(TOTAL_COUNT, int(dt.strftime("%s")))
  print(costs)

  ac_temps = [float(x) for x in main(alpha, beta, env_temps, room_temp,
              min_temp, max_temp, costs)['x']]
  print(ac_temps)


  print(calculate_eff(alpha, beta, room_temp, min_temp, max_temp,
                      env_temps, costs, ac_temps, TOTAL_COUNT))

