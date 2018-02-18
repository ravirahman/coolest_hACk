import csv
import parsedatetime
import datetime


cal = parsedatetime.Calendar()

scores = []
times = []
with open('price.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    dt = cal.parse(row[0])[0]
    dt = datetime.datetime(dt[0], dt[1], dt[2], dt[3], dt[4])
    times.append(int(dt.strftime("%s")))
    scores.append(row[1])

def get_cost_proj(unix_time):
  for i, tm in enumerate(times):
    if tm > unix_time:
      return [float(x) for x  in scores[i:i+4]]

