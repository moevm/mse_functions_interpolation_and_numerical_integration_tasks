import numpy as np
from numpy import random as nprd
from random import sample
import random

class Polynomial:
    degree = None

    def __init__(self, degree, seed=None):
        random.seed(seed, version=2)
        nprd.seed(seed)

        self.x = []
        self.y = []

        while len(self.x) != degree + 1:
            self.coefficients = nprd.randint(-10, 11, degree + 1)
            x = np.arange(-20, 21)
            y = self.f(x)
            x = x[np.logical_and(-60 <= y, y <= 60)]

            # если нам не хватает подходящих пар x и y заново генерим коэфициенты многочлена
            if len(x) < degree + 1:
                continue
            else:
                self.x = sorted(sample(x.tolist(), degree + 1))
                self.y = list(map(self.f, self.x))

    def __eq__(self, obj):
        return isinstance(obj, Polynomial) and obj.x == self.x and obj.y == self.y

    def f(self, x):
        y = 0
        for i, coefficient in enumerate(self.coefficients):
            y += coefficient * pow(x, i)
        return y
