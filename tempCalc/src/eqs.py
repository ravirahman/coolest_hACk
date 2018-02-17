import math
import numpy as np
from scipy.optimize import minimize, basinhopping


def get_best(alpha=-0.05, beta=-0.2, env_temp=90, init_temp=65, min_temp=60, max_temp=65, cost=[10, 15, 30, 60], debug=False):
  n_segments = len(cost)
  
  def to_optimize(ac_temps):
    total = 0
    for i in range(n_segments): total += abs(env_temp - ac_temps[i]) * cost[i]
    return total

  def room_temp(ac_temp, last_temp, t):
    env_comp = (alpha * env_temp) / (alpha + beta)
    ac_comp = (beta * ac_temp) / (alpha + beta)
    C = last_temp - env_comp - ac_comp
    return env_comp + ac_comp + C * math.exp(alpha * t + beta * t)

  cons = []
  def room_temp_f(n, ac_temps):
    if n is -1:
      return lambda t: init_temp
    temp_f = lambda t, y=n: room_temp(ac_temps[y], room_temp_f(y - 1, ac_temps)(t), t)
    return temp_f

  for i in range(n_segments):
    cons.append(lambda temps, y=i: temps[y])
    cons.append(lambda temps, y=i: room_temp_f(y, temps)(15) - min_temp)
    cons.append(lambda temps, y=i: max_temp - room_temp_f(y, temps)(15))

  x0 = [init_temp] * n_segments
  cons = [{'type': 'ineq', 'fun': f} for f in cons]
  
  return minimize(to_optimize, x0, method='COBYLA', constraints=cons)

print(get_best())
scores = [int(x) for x in get_best()['x']]
print(scores)

