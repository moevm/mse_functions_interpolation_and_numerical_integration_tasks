import numpy as np
from numpy.polynomial import Polynomial as P
from numpy import random
from pylatex import Document, NewPage, Command, Package, UnsafeCommand, Center, Tabular, MultiRow
from pylatex.utils import NoEscape, italic, bold


class InterpolationTask:
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
            self.coefficients = np.round(random.uniform(-10, 10, degree + 1), 1)

            if self.degree in [5, 6]:
                step = 1
                x = np.arange(-30, 31)
            else:
                step = random.choice([2, 3, 4])
                x = np.arange(-30, 31, step)

            while np.any(self.coefficients == 0):
                self.coefficients = np.round(random.uniform(-10, 10, degree + 1), 1)

            p = P(self.coefficients)
            y = p(x)
            mask = np.logical_and(-500 <= y, y <= 500)

            # если нам не хватает подходящих пар x и y заново генерим коэфициенты многочлена
            if np.sum(mask) < degree + 1:
                continue
            else:
                self.x = list(x[mask][:degree + 1])
                self.y = list(np.round(y[mask][:degree + 1]))


    def __eq__(self, obj):
        return isinstance(obj, InterpolationTask) and obj.x == self.x and obj.y == self.y

    def get_table(self):
        # Table with values
        table = Tabular(table_spec='c'.join(["|" for _ in range(self.degree + 3)]))
        table.add_hline()
        table.add_row(['$x_i$'] + self.x, escape=False)
        table.add_hline()
        table.add_row(['$y_i$'] + self.y, escape=False)
        table.add_hline()
        center = Center()
        center.append(table)
        return center

    def get_tex_text(self, task_number):
        task_table = Tabular("p{9cm}")

        # Task text
        task_text = NoEscape("\\hspace{5mm}" + bold(f"{task_number}). ")
                               + NoEscape(r'Построить интерполяционный многочлен в')
                               + italic(' форме Лагранжа') + ', в ' + italic('форме Ньютона')
                               + ' и сравнить результаты.')
        task_table.append(task_text)

        # Table with values
        task_table.append(self.get_table())

        return task_table

    def get_tex_answer(self, task_number):
        answer_table = Tabular("p{9cm}")

        answer_table.append(f'Ответ для {task_number}-го номера')

        answer_table.append(self.get_table())

        center = Center()
        num = len(self.coefficients) - 1
        result = "$L_" + str(num) + "(x) = "
        for i, coefficient in enumerate(self.coefficients):
            if coefficient != 0:
                if i == 0:
                    result += f"{coefficient}"
                elif i == 1:
                    if coefficient != 1:
                        result += f"{coefficient}x"
                    else:
                        result += "x"
                else:
                    if coefficient != 1:
                        result += f"{coefficient}x^{i}"
                    else:
                        result += f"x^{i}"

            if i != len(self.coefficients) - 1:
                if self.coefficients[i + 1] > 0:
                    result += "+"
        result += "$"
        center.append(NoEscape(result))

        answer_table.append(center)
        return answer_table
