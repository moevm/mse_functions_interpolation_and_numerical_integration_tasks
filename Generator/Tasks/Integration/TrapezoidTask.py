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
    def randomize(self, dotsCnt):

        if type(dotsCnt) != int:
            return None

        firstX = random.randint(-10, 10)

        step = random.choice([0.1, 0.2, 0.3])
        self.xValues = [i * step + firstX for i in range(dotsCnt)]

        self.n = dotsCnt

        half = int((dotsCnt - 2) / 2)

        self.yValues.append(round(random.uniform(-9, 9), 1))
        for _ in range(1, half + 1):
            new_elem = round(random.uniform(-9, 9), 1)
            while new_elem in self.yValues:
                new_elem = round(random.uniform(-9, 9), 1)
            self.yValues.append(new_elem)

        tmp = self.yValues[1::]
        tmp.reverse()
        self.yValues += tmp
        self.yValues.append(0)

        coef = round(random.uniform(-4, 4), 1) + 1
        self.yValues[-1] += coef
        self.yValues[-2] += coef

        self.yValues.append(round(random.uniform(-9, 9), 1))

        res = abs(self.yValues[0] + self.yValues[-1]) * step / 2
        while res > 0.2 or res == 0:
            self.yValues[-1] = round(random.uniform(-9, 9), 1)
            res = abs(self.yValues[0] + self.yValues[-1]) * step / 2

        self.answer = trapezoid(self.yValues, step)
        self.halfAnswer = trapezoid(self.yValues[::2], step * 2)

        return self

    def errorRunge(self):
        return abs(self.halfAnswer - self.answer) / 3

    def taskText(self, task_number):
        return NoEscape(
            r"\hspace{5mm}" + bold(f"{task_number}). ") + "Вычислить приближённое значение " +
            r"$\int_{" + "{0:.1f}".format(self.xValues[0]) + "}^{" + "{0:.1f}".format(
                self.xValues[-1]) + "}f(x)dx$" + r"\hspace{1mm}от таблично заданной функции по "
            + italic("формуле трапеций ") + "по " + d[int(self.n / 2) + self.n % 2]
            + " и по " + d[self.n] + " узлам." +
            " Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")

    def answerStr(self):
        return NoEscape(
            "$S_" + str(int(self.n / 2) + len(self.yValues) % 2) + "=" + "{0:.2f}".format(
                self.halfAnswer) +
            r"\rightarrow" + "{0:.2f}".format(self.answer) + r"\rightarrow" +
            "{0:.3f}".format(
                self.answer + (self.answer - self.halfAnswer) / 3) + r"$\hspace{1mm}(трапеции)")
