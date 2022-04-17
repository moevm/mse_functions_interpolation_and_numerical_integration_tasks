from pylatex.utils import NoEscape
from pylatex import Tabular, Center
import numpy
from numpy import random


class SplineTask:
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
        self.answer = self.solve()

    @classmethod
    def randomize(cls, x_range=(-5, 5), y_range=(-20, 20),
                  step=1):
        center_x = random.randint(x_range[0], x_range[1] + 1)
        x_values = [center_x + step * i for i in range(-1, 2)]

        y_values = [round(random.uniform(y_range[0], y_range[1]), 1) for _ in range(3)]

        return cls(x_values, y_values)

    def get_tex_text(self):
        main_table = Tabular("p{9cm}")
        task_text_1 = NoEscape("\\hspace{5mm} Дана таблица значений функции ($ i = 0, \dots, 2 $):")

        main_table.append(task_text_1)

        valueCnt = len(self.x_values)
        valueStartPoint = 0
        tableView = "|l|"
        tableView += "l|" * valueCnt
        table = Tabular(tableView)
        table.add_hline()
        table.add_row(
            [NoEscape("$ x_i $")] + [NoEscape("${0:.1f}$".format(self.x_values[i])) for i in
                                     range(valueStartPoint, valueStartPoint + valueCnt)])
        table.add_hline()
        table.add_row(
            [NoEscape("$ f_i $")] + [NoEscape("${0:.1f}$".format(self.y_values[i])) for i in
                                     range(valueStartPoint, valueStartPoint + valueCnt)])
        table.add_hline()

        center = Center()
        center.append(table)
        main_table.append(center)

        task_text_2 = NoEscape(
            "\\hspace{5mm} Необходимо построить параболический сплайн $ S_2(x) $ дефекта " +
            "1 при граничном условии $ {S'_2(x_0)=0} $.")

        main_table.append(task_text_2)
        return main_table

    def get_polynomial_strings(self):
        string_1 = ""
        string_2 = ""

        if round(self.answer[0], 1) != 0:
            string_1 += "{0:.1f}".format(self.answer[0])
        if round(self.answer[1], 1) != 0:
            if len(string_1) != 0:
                string_1 += "{0:+.1f} \cdot x".format(abs(self.answer[1]))
            else:
                string_1 += "{0:.1f} \cdot x".format(abs(self.answer[1]))
        if round(self.answer[2], 1) != 0:
            if len(string_1) != 0:
                string_1 += "{0:+.1f} \cdot x^2".format(abs(self.answer[2]))
            else:
                string_1 += "{0:.1f} \cdot x^2".format(abs(self.answer[2]))
        if string_1 == "":
            string_1 += "{0:.1f}".format(0)

        if round(self.answer[3], 1) != 0:
            string_2 += "{0:.1f}".format(self.answer[3])
        if round(self.answer[4], 1) != 0:
            if len(string_2) != 0:
                string_2 += "{0:+.1f} \cdot x".format(abs(self.answer[4]))
            else:
                string_2 += "{0:.1f} \cdot x".format(abs(self.answer[4]))
        if round(self.answer[5], 1) != 0:
            if len(string_2) != 0:
                string_2 += "{0:+.1f} \cdot x^2".format(abs(self.answer[5]))
            else:
                string_2 += "{0:.1f} \cdot x^2".format(abs(self.answer[5]))
        if string_2 == "":
            string_2 += "{0:.1f}".format(0)

        string_1 += ",x \in [{0:.1f}, {1:.1f}]".format(self.x_values[0], self.x_values[1])
        string_2 += ",x \in [{0:.1f}, {1:.1f}]".format(self.x_values[1], self.x_values[2])
        return [string_1, string_2]

    def get_tex_answer(self, task_number, seed=None):
        p0 = f'Ответ для {task_number}-го номера'
        if seed is not None:
            p0 += f' ({seed})'

        p1, p2 = self.get_polynomial_strings()
        return NoEscape(p0) + NoEscape(':') + NoEscape(r"\newline") + NoEscape("$S_2(x) = $") + \
               NoEscape("$\\begin{cases}") + \
               NoEscape(p1) + NoEscape(r'\\') + NoEscape(p2) + NoEscape(r"\\") + \
               NoEscape("\\end{cases}$")

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
