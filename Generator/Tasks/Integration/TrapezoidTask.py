from numpy import random
from pylatex.utils import NoEscape, bold, italic
from Tasks.Integration.IntegrationTask import IntegrationTask


def trapezoid(y, h):
    res = (y[0] + y[-1]) / 2

    for i in range(1, len(y) - 1):
        res += y[i]

    res *= h

    return res


d = {
    1: "одному",
    2: "двум",
    3: "трем",
    4: "четырем",
    5: "пяти",
    6: "шести",
    7: "семи",
    8: "восьми",
    9: "девяти",
    10: "десяти",
    11: "одиннадцати",
    12: "двенадцати",
    13: "тринадцати",
    14: "четырнадцати",
    15: "пятнадцати",
    16: "шестнадцати",
    17: "семнадцати",
    18: "восемнадцати",
    19: "девятнадцати",
    20: "двадцати"
}


class TrapezoidTask(IntegrationTask):
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
        step = x_values[1] - x_values[0]
        self.answer = trapezoid(self.y_values, step)
        self.halfAnswer = trapezoid(self.y_values[::2], step * 2)

    @classmethod
    def randomize(cls, points_count):
        if type(points_count) != int:
            return None
        first_x = random.randint(-10, 10)
        step = random.choice([0.1, 0.2, 0.3])
        x_values = [i * step + first_x for i in range(points_count)]
        y_values = [round(random.uniform(-9, 9), 1)]

        minus_y = []
        plus_y = []
        for _ in range(int((points_count - 2) / 2) - 1):
            while True:
                y_first = round(random.uniform(-9, 9), 1)
                y_second = y_first
                if y_first not in minus_y:
                    break
            minus_y.append(y_first)
            plus_y.append(y_second)

        random.shuffle(minus_y)
        random.shuffle(plus_y)
        for _ in range(len(minus_y)):
            offset = round(random.uniform(-0.9, 1), 1)
            y_values.append(minus_y.pop() + offset)
            y_values.append(plus_y.pop() + offset)

        difference = 0
        while -0.1 < difference < 0.1:
            difference = round(random.uniform(-0.5, 0.5), 1)

        if points_count % 2 != 0:
            if points_count == 3:
                y_values.append(0)
            else:
                y_first = round(random.uniform(-4.5, 4.5), 1)
                y_third = round(random.uniform(-4.5, 4.5), 1)
                y_second = y_first + y_third
                y_values.append(y_first)
                y_values.append(y_second)
                y_values.append(y_third)

            y_values.append(difference * 2 / step - y_values[0])
        else:
            y_pre_last = round(random.uniform(-4.5, 4.5), 1)
            y_values.append(y_pre_last)
            y_values.append(round(random.uniform(-9, 9), 1))
            y_last = -y_pre_last + 1/2 * y_values[0] - difference/step
            y_values.append(round(y_last, 1))

        return cls(x_values, y_values)

    def error_runge(self):
        return abs(self.halfAnswer - self.answer) / 3

    def task_text(self, task_number):
        return NoEscape(
            r"\hspace{5mm}" + bold(f"{task_number}). ") + "Вычислить приближённое значение " +
            r"$\int_{" + "{0:.1f}".format(self.x_values[0]) + "}^{" + "{0:.1f}".format(
                self.x_values[-1]) + "}f(x)dx$" + r"\hspace{1mm}от таблично заданной функции по "
            + italic("формуле трапеций ") + "по " + d[int(len(self.x_values) / 2) + len(self.x_values) % 2]
            + " и по " + d[len(self.x_values)] + " узлам." +
            " Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")

    def answer_str(self):
        return NoEscape(
            "$S_" + str(int(len(self.x_values) / 2) + len(self.y_values) % 2) + "=" + "{0:.2f}".format(
                self.halfAnswer) +
            r"\rightarrow" + "{0:.2f}".format(self.answer) + r"\rightarrow" +
            "{0:.3f}".format(
                self.answer + (self.answer - self.halfAnswer) / 3) + r"$\hspace{1mm}(трапеции)")
