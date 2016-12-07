import numpy as np
import math
import random
import pandas as pd


def func(x, a, b, c):
    return np.array([a * math.exp(-math.exp(b - c * xx)) for xx in x])


def true_form(item, beta):
    return beta[0] * math.exp(-math.exp(beta[1] - beta[2] * item))


x = np.array([x * 1.0 / 1000 for x in range(0, 1000, 1)])
y = np.array([true_form(s, [1.02, 1.46, 5.1]) + random.sample([1, -1], 1)[0] * random.random() / 4 for s in x])

df = pd.DataFrame({'time': pd.Series(x), 'complete': pd.Series(y)})
df.to_csv('data.csv')
#
# errors = np.array([math.pow(10, -8) for i in x])
# initial_value = np.array([1.02, 1.46, 5.1])
#
# result = optimization.curve_fit(func, x, y, initial_value, errors, method='lm')
# beta = result[0]
#
# plt.figure()
# plt.plot(x, y, 'r.')
# plt.plot(x, [true_form(xx, beta) for xx in x], 'b')
# plt.show()
