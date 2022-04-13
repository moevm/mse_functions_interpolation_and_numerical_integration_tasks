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
    def randomize(self, dotsCnt):

        if type(dotsCnt) != int:
            return None

        firstX = random.randint(-10, 10)

        step = 0.6
        self.xValues = [i * step + firstX for i in range(dotsCnt)]

        self.n = dotsCnt

        self.yValues.append(round(random.uniform(-9, 9), 1))
        self.yValues += self.generate_middle_values()

        self.yValues.append(round(random.uniform(-9, 9), 1))
        res = abs(self.yValues[0] + self.yValues[-1]) * step / 3
        while res > 0.2 or res == 0:
            self.yValues[-1] = round(random.uniform(-9, 9), 1)
            res = abs(self.yValues[0] + self.yValues[-1]) * step / 3

        self.answer = simpson(self.yValues, step)
        self.halfAnswer = simpson(self.yValues[::2], step * 2)

        return self

    def generate_middle_values(self):
        values = []
        number_of_values = self.n - 2

        if number_of_values == 1:
            return [0]

        # answer_2h - answer_h = (y0 - 4*y1 + 6*y2 - 4*y3 + 2*y4 - 4*y5 + 6*y6 - 4*y7 +
        #                                                                    + ... + y_last) * h/3
        # Goal: (-4*y1 + 6*y2 - 4*y3) + (2*y4 - 4*y5) + (6*y6 - 4*y7) + ... = 0
        # answer_2h - answer_h = (y0 + y_last) * h/3

        # Generate first 3 values
        value1 = round(random.uniform(-4.5, 4.5), 1)
        value2 = round(random.uniform(-3, 3), 1)
        if int(value2 * 10) % 2 == 1:
            value2 = round(value2 + 0.1, 1)

        number_of_values -= 3

        # Three types of y
        minus_four_coefficient = []
        six_coefficient = []
        two_coefficient = []

        # -4*y1 + 6*y2 + -4*y3 = 0
        # y3 = -y1 + 3/2 * y2
        minus_four_coefficient.append(value1)
        six_coefficient.append(value2)
        minus_four_coefficient.append(round(-value1 + 3 / 2 * value2, 1))

        for i in range(int(number_of_values / 2)):
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

        values.append(minus_four_coefficient.pop())
        values.append(six_coefficient.pop())
        values.append(minus_four_coefficient.pop())

        for i in range(int(number_of_values / 2)):
            if i % 2 == 0:
                values.append(two_coefficient.pop())
                values.append(minus_four_coefficient.pop())
            else:
                values.append(six_coefficient.pop())
                values.append(minus_four_coefficient.pop())

        return values

    def errorRunge(self):
        return abs(self.halfAnswer - self.answer) / 15

    def taskText(self, task_number):
        return NoEscape(
            r"\hspace{5mm}" + bold(f'{task_number}). ') + "Вычислить приближённое значение " +
            r"$\int_{" + "{0:.1f}".format(self.xValues[0]) + "}^{" + "{0:.1f}".format(
                self.xValues[-1]) + "}f(x)dx$" \
                                    r"\hspace{1mm}от таблично заданной функции по "
            + italic("формуле Симпсона ") + "по " + d[int(self.n / 2) + self.n % 2] +
            " и по " + d[self.n] + " узлам." +
            " Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")

    def answerStr(self):
        return NoEscape(
            "$S_" + str(int(self.n / 2) + len(self.yValues) % 2) + "=" + "{0:.3f}".format(
                self.halfAnswer) +
            r"\rightarrow" + "{0:.3f}".format(self.answer) + r"\rightarrow" +
            "{0:.3f}".format(
                self.answer + (self.answer - self.halfAnswer) / 15) + r"$\hspace{1mm}(Симпсон)")
