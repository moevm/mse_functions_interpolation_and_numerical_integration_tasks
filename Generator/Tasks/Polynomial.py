import numpy as np
from numpy.polynomial import Polynomial as P
from numpy import random


class Polynomial:
    def __init__(self, degree, seed=None):
        self.degree = degree

        if seed is not None:
            random.seed(seed)
        self.x = [0, 1]
        self.y = []
        step = None

        while True:
            if len(self.x) == degree + 1 and np.all(np.diff(self.x) == step):
                break
            self.coefficients = np.round(random.uniform(-10, 10, degree+1), 1)

            if self.degree in [5, 6]:
                step = 1
                x = np.arange(-30, 31)
            else:
                step = random.choice([2, 3, 4])
                x = np.arange(-30, 31, step)

            while np.any(self.coefficients == 0):
                self.coefficients = np.round(random.uniform(-10, 10, degree+1), 1)

            p = P(self.coefficients)
            y = p(x)
            mask = np.logical_and(-500 <= y, y <= 500)

            # если нам не хватает подходящих пар x и y заново генерим коэфициенты многочлена
            if np.sum(mask) < degree + 1:
                continue
            else:
                self.x = list(x[mask][:degree + 1])
                self.y = list(np.round(y[mask][:degree + 1]))

        print(self.x)

    def __eq__(self, obj):
        return isinstance(obj, Polynomial) and obj.x == self.x and obj.y == self.y
