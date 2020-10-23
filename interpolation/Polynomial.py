import numpy as np
from numpy import random
from random import sample

class Polynomial:
    degree = None

    def __init__(self, degree):
        self.x = []
        self.y = []

        while len(self.x) != degree + 1:
            self.coefficients = random.randint(-10, 11, degree + 1)
            x = np.arange(-20, 21)
            y = self.f(x)
            tmp_x = x[np.logical_and(-60 <= y, y <= 60)]

            # если нам не хватает подходящих пар x и y заново генерим коэфициенты многочлена
            if len(tmp_x) < degree + 1:
                continue
            else:
                self.x = sample(tmp_x.tolist(), degree + 1)
                self.y = list(map(self.f, self.x))

    def f(self, x):
        y = 0
        for i, coefficient in enumerate(self.coefficients):
            y += coefficient * pow(x, i)
        return y
