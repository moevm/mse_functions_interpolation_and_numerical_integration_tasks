import numpy
from numpy import random
 
 
class SplineTask:
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
        self.answer = self.solve()
 
    @classmethod
    def randomize(cls, seed=None, x_range=(-5, 5), y_range=(-20, 20),
                  step=1, middle_is_zero=False):
        if seed is not None:
            random.seed(seed)
 
        if middle_is_zero:
            center_x = 0
        else:
            center_x = random.randint(x_range[0], x_range[1])
        x_values = [center_x + step * i for i in range(-1, 2)]
 
        y_values = [round(random.uniform(y_range[0], y_range[1]), 1) for _ in range(3)]
 
        return cls(x_values, y_values)
 
    def solve(self):
        a_matrix = numpy.array([[1, self.x_values[0], self.x_values[0] ** 2, 0, 0, 0],
                                [1, self.x_values[1], self.x_values[1] ** 2, 0, 0, 0],
                                [0, 0, 0, 1, self.x_values[1], self.x_values[1] ** 2],
                                [0, 0, 0, 1, self.x_values[2], self.x_values[2] ** 2],
                                [0, 1, 2 * self.x_values[1], 0, -1, -2 * self.x_values[1]],
                                [0, 1, 2 * self.x_values[0], 0, 0, 0]])
 
        b_matrix = numpy.array([self.y_values[0],
                                self.y_values[1],
                                self.y_values[1],
                                self.y_values[2],
                                0,
                                0])
 
        return numpy.linalg.solve(a_matrix, b_matrix)