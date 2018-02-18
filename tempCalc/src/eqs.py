import math
from scipy.optimize import minimize


def calc_temp(alpha, beta, ac_temp, env_temp, last_temp, t):
  '''
  Calculate projected room temperature.
  '''

  term1 = (alpha * env_temp) / (alpha + beta)
  term2 = (beta * ac_temp) / (alpha + beta)
  C = last_temp - term1 - term2
  return term1 + term2 + C * math.exp(-alpha * t + -beta * t)


def calc_naive(alpha, beta, env_temp, last_temp, min_temp, max_temp):
  '''
  Calculate naively extrapolated AC temps.
  '''

  if env_temp < min_temp:
    for i in range(50):
      if calc_temp(alpha, beta, min_temp + i, env_temp,
                   last_temp, 15) > min_temp:
        return min_temp + i
    return min_temp + 50
  elif env_temp > max_temp:
    for i in range(50):
      if calc_temp(alpha, beta, max_temp - i, env_temp, last_temp,
                   15) < max_temp:
        return max_temp - i
    return max_temp - 50
  else:
    return env_temp


def calc_cost(costs, env_temps, ac_temps):
  '''
  Calculate cost of energy
  '''

  total = 0
  for i, cost in enumerate(costs):
    total += abs(env_temps[i] - ac_temps[i]) * cost
  return total


def main(alpha=0.009, beta=0.1, env_temps=[90, 70, 90, 100],
         init_temp=90, min_temp=50, max_temp=70, costs=[5, 5, 5, 5],
         debug=False):
  '''
  Calculate requested AC temperature.
  '''

  # Define optimize functions
  def to_optimize(ac_temps):
    calc_cost(costs, env_temps, ac_temps)

  # Define room temp calculator
  def room_temp(n, ac_temps):
    if n is -1:
      return lambda t: init_temp
    return lambda t: calc_temp(alpha, beta, ac_temps[n], env_temps[n],
                               room_temp(n - 1, ac_temps)(15), t)

  # Define constraints
  cons = []
  for i in range(len(costs)):
    cons.append(lambda temps, y=i: room_temp(y, temps)(15) - min_temp)
    cons.append(lambda temps, y=i: max_temp - room_temp(y, temps)(15))

  # Establish optim params
  x0 = [init_temp] * len(costs)
  cons = [{'type': 'ineq', 'fun': f} for f in cons]

  return minimize(to_optimize, x0, method='COBYLA', constraints=cons)

