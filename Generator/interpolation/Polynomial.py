import numpy as np
from numpy import random


class Polynomial:
    def __init__(self, degree, seed=None):
        self.degree = degree

        step = random.choice([2, 3, 4])
        if seed is not None:
            random.seed(seed)
        self.x = [0, 1]
        self.y = []

        while True:
            if len(self.x) == degree + 1 and np.all(np.diff(self.x) == step):
                break
            self.coefficients = random.randint(-10, 11, degree + 1)
            x = np.arange(-30, 31, step)
            y = self.f(x)
            mask = np.logical_and(-500 <= y, y <= 500)

            # если нам не хватает подходящих пар x и y заново генерим коэфициенты многочлена
            if np.sum(mask) < degree + 1:
                continue
            else:
                self.x = list(x[mask][:degree + 1])
                self.y = list(y[mask][:degree + 1])

    def __eq__(self, obj):
        return isinstance(obj, Polynomial) and obj.x == self.x and obj.y == self.y

    def f(self, x):
        y = 0
        for i, coefficient in enumerate(self.coefficients):
            y += coefficient * np.power(x, i)
        return y
