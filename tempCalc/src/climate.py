from forecastiopy import *
import datetime

apikey = "d057f5b3b90154e47107070d1aecf47c"
Stanford = [37.4248, -122.1677]

fio = ForecastIO.ForecastIO(apikey,
                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
                            latitude=Stanford[0], longitude=Stanford[1])

def get_temps(TOTAL_COUNT):
  hourly = FIOHourly.FIOHourly(fio)
  min = datetime.datetime.now().minute
  if min < 20:
    l = hourly.get_hour(0)['temperature']
    r = hourly.get_hour(1)['temperature']
  elif min > 40:
    l = hourly.get_hour(1)['temperature']
    r = hourly.get_hour(2)['temperature']
  else:
    l = (hourly.get_hour(0)['temperature'] + hourly.get_hour(1)['temperature']) / 2
    r = (hourly.get_hour(1)['temperature'] + hourly.get_hour(2)['temperature']) / 2
  s = (r - l) / 60
  ts = []
  for i in range(TOTAL_COUNT):
    ts.append(l + s * (i * 60 / TOTAL_COUNT))
  return ts

