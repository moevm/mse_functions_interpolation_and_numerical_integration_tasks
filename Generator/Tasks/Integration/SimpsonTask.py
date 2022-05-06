from numpy import random
from pylatex.utils import NoEscape, bold, italic
from Tasks.Integration.IntegrationTask import IntegrationTask


def simpson(y, h):
    res = y[0] + y[-1]

    for i in range(1, len(y) - 1):
        res += 4 * y[i] if i % 2 == 1 else 2 * y[i]

    res *= h / 3

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


class SimpsonTask(IntegrationTask):
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
        step = x_values[1] - x_values[0]
        self.answer = simpson(self.y_values, step)
        self.halfAnswer = simpson(self.y_values[::2], step * 2)

    @classmethod
    def randomize(cls, points_count):
        if type(points_count) != int:
            return None
        first_x = random.randint(-10, 10)
        step = 0.6
        x_values = [i * step + first_x for i in range(points_count)]
        y_values = [round(random.uniform(-6, 6), 1)]

        if points_count == 3:
            return y_values.append(0)
        else:
            # answer_2h - answer_h = (y0 - 4*y1 + 6*y2 - 4*y3 + 2*y4 - 4*y5 + 6*y6 - 4*y7 +
            #                                                                    + ... + y_last) * h/3
            # Goal: (-4*y1 + 6*y2 - 4*y3) + (2*y4 - 4*y5) + (6*y6 - 4*y7) + ... = 0
            # difference = answer_2h - answer_h = (y0 + y_last) * h/3
            # y_last = y0 - (3*difference)/h

            # Generate first 3 values
            value1 = round(random.uniform(-4.5, 4.5), 1)
            value2 = round(random.uniform(-3, 3), 1)
            if int(value2 * 10) % 2 == 1:
                value2 = round(value2 + 0.1, 1)

            # Three types of y
            minus_four_coefficient = []
            six_coefficient = []
            two_coefficient = []

            # -4*y1 + 6*y2 + -4*y3 = 0
            # y3 = -y1 + 3/2 * y2
            minus_four_coefficient.append(value1)
            six_coefficient.append(value2)
            minus_four_coefficient.append(round(-value1 + 3 / 2 * value2, 1))

            for i in range(int(points_count - 5 / 2)):
                if i % 2 == 0:
                    # 2*y4 - 4*y5 = 0
                    # y4 = 2*y5
                    value = round(random.uniform(-4.5, 4.5), 1)
                    two_coefficient.append(round(value * 2, 1))  # y4
                    minus_four_coefficient.append(value)  # y5
                else:
                    value = round(random.uniform(-6, 6), 1)
                    if int(value * 10) % 2 == 1:
                        value = round(value + 0.1, 1)

                    # 6*y6 - 4*y7 = 0
                    # y7 = 3/2 * y6
                    six_coefficient.append(value)  # y6
                    minus_four_coefficient.append(round(3 / 2 * value, 1))  # y7

            # Shuffle values to make dependency on each other less obvious
            random.shuffle(minus_four_coefficient)
            random.shuffle(two_coefficient)
            random.shuffle(six_coefficient)

            y_values.append(minus_four_coefficient.pop())
            y_values.append(six_coefficient.pop())
            y_values.append(minus_four_coefficient.pop())

            for i in range(int(points_count - 5 / 2)):
                if i % 2 == 0:
                    y_values.append(two_coefficient.pop())
                    y_values.append(minus_four_coefficient.pop())
                else:
                    y_values.append(six_coefficient.pop())
                    y_values.append(minus_four_coefficient.pop())

        difference = 0
        while -0.1 < difference < 0.1:
            difference = round(random.uniform(-0.5, 0.5), 1)

        y_values.append(round(y_values[0] - (3 * difference) / step, 1))

        return cls(x_values, y_values)

    def error_runge(self):
        return abs(self.halfAnswer - self.answer) / 15

    def task_text(self, task_number):
        return NoEscape(
            r"\hspace{5mm}" + bold(f'{task_number}). ') + "Вычислить приближённое значение " +
            r"$\int_{" + "{0:.1f}".format(self.x_values[0]) + "}^{" + "{0:.1f}".format(
                self.x_values[-1]) + "}f(x)dx$" \
                                     r"\hspace{1mm}от таблично заданной функции по "
            + italic("формуле Симпсона ") + "по " + d[int(len(self.x_values) / 2) + len(self.x_values) % 2] +
            " и по " + d[len(self.x_values)] + " узлам." +
            " Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")

    def answer_str(self):
        return NoEscape(
            "$S_" + str(int(len(self.x_values) / 2) + len(self.y_values) % 2) + "=" + "{0:.2f}".format(
                self.halfAnswer) +
            r"\rightarrow" + "{0:.2f}".format(self.answer) + r"\rightarrow" +
            "{0:.3f}".format(
                self.answer + (self.answer - self.halfAnswer) / 15) + r"$\hspace{1mm}(Симпсон)")
