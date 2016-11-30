import numpy as np
import math
from scipy.optimize import least_squares


def get_parameter(x, y):
    t0 = np.random.rand(3)
    res = least_squares(growth_func, t0, args=(x, y))
    return res.x


def growth_func(t, x, y):
    return t[0] * math.exp(-math.exp(t[1] - t[2] * x)) - y


if __name__ == "__main__":
    print get_parameter(0, 0.1)
    print get_parameter(0.1, 0.15)
    print get_parameter(0.2, 0.2)
    print get_parameter(0.4, 0.5)

