import csv
import numpy as np
import parsedatetime
from sklearn import svm
from sklearn.utils import shuffle
from sklearn.metrics import mean_absolute_error


cal = parsedatetime.Calendar()

scores = []
times = []

with open('full.csv', 'r') as f:
  reader = csv.reader(f)
  i = 0
  for row in reader:
    if i is 4000:
      break
    dt = cal.parse(row[0])[0]
    times.append([dt[3], dt[1]])
    scores.append(float(row[1]))
    i += 1


def slidingWindow(sequence, winSize, step=1):
    """Returns a generator that will iterate through
    the defined chunks of input sequence.  Input sequence
    must be iterable."""

    global times

    # Pre-compute number of chunks to emit
    numOfChunks = int((len(sequence) - winSize) / step) + 1
    # Do the work
    for i in range(0, numOfChunks * step, step):
        yield sequence[i:i + winSize], times[i + winSize - 1]


windows = slidingWindow(scores, 20, 2)
X = []
Y = []
for window, dt in windows:
  X.append(window[:-1] + dt)
  Y.append(window[-1])
X = np.array(X, dtype=np.float16)
Y = np.array(Y, dtype=np.float16)
X, Y = shuffle(X, Y)

print(X)
print(Y)
del(windows)
del(scores)
del(times)

print("Ready")
clf = svm.SVR()
clf.fit(X[:-100], Y[:-100])

pred = clf.predict(X[-100:])
print(pred)
print(mean_absolute_error(pred, Y[-100:]))

