import numpy as np
from numpy import random

class Polynomial:
    degree = None

    def __init__(self, degree, seed=None):
        self.degree = degree
        step = random.choice([2, 3, 4])
        if seed is not None:
            random.seed(seed)
        self.x = [0, 1]
        self.y = []

        while True:
            if len(self.x) == degree + 1 and self.check_difference(step):
                break
            self.coefficients = random.randint(-10, 11, degree + 1)
            x = np.arange(-10, 51)
            y = self.f(x)
            x = x[np.logical_and(-500 <= y, y <= 500)]

            # если нам не хватает подходящих пар x и y заново генерим коэфициенты многочлена
            if len(x) < degree + 1:
                continue
            else:
                self.x = sorted(random.choice(x.tolist(), degree + 1, replace=False))
                self.y = list(map(self.f, self.x))

    def __eq__(self, obj):
        return isinstance(obj, Polynomial) and obj.x == self.x and obj.y == self.y

    def f(self, x):
        y = 0
        for i, coefficient in enumerate(self.coefficients):
            y += coefficient * pow(x, i)
        return y

    def check_difference(self, difference):
        for i in range(1, len(self.x)):
            if self.x[i] - self.x[i-1] != difference:
                return False
        return True
