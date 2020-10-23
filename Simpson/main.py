from random import randint
from random import choice
from pylatex import Document, Tabular, Package, NewLine, Math
from pylatex.utils import bold, NoEscape, italic


class Task:
    def __init__(self):
        self.xValues = []
        self.yValues = []
        self.answer = 0

    def randomize(self, dotsCnt):
        hDenominator = choice([2, 5, 10, 20])
        resDenominator = hDenominator * 3

        a = randint(-1, 1)
        self.xValues = [a + i * (1 / hDenominator) for i in range(dotsCnt)]

        while True:
            self.yValues = [randint(-30, 30) for i in range(dotsCnt)]
            self.answer = simpson(self.yValues, hDenominator)
            if abs(self.answer) < 100:
                return self

    def addTexAnswer(self, ind, answerDoc):
        answerDoc.append(NoEscape(r"\noindent{0}: {1}".format(ind, self.answer)))
        answerDoc.append(NewLine())

    def addTexTask(self, taskDoc):
        tableView = "|c|"
        tableView += "c|" * len(self.xValues)

        taskDoc.append(NoEscape(r"\noindent"))
        taskDoc.append(NoEscape(r"2)\hspace{2mm}Вычислить  приближенное значение"))
        taskDoc.append(NoEscape(r"$\int_{" + "{0:.1f}".format(self.xValues[0]) + "}^{" +
                                "{0:.1f}".format(self.xValues[-1]) + "}f(x)dx$"))
        taskDoc.append(NoEscape(r"\hspace{1mm} от таблично заданной функции по "))
        taskDoc.append(italic("формуле Симпсона"))
        taskDoc.append(NoEscape(r"\hspace{1mm}по пяти и по девяти узлам. Оценить погрешность по правилу Рунге;"
                                r" уточнить результат по Ричардсону.\vspace{5mm}\newline"))

        with taskDoc.create(Tabular(tableView)) as table:
            table.add_hline()
            table.add_row(["x"] + ["{0:.1f}".format(i) for i in self.xValues])
            table.add_hline()
            table.add_row(["y"] + self.yValues)
            table.add_hline()
        taskDoc.append(NoEscape(r"\vspace{12mm}"))
        taskDoc.append(NewLine())


def simpson(y, resDenominator):
    res = y[0]

    for i in range(1, len(y) - 1):
        if i % 2 == 1:
            res += 4 * y[i]
        else:
            res += 2 * y[i]

    y[-1] = resDenominator - res % resDenominator
    res += y[-1]

    res /= resDenominator

    return res


tasks = [Task().randomize(9) for i in range(10)]

answerDoc = Document("answers")
taskDoc = Document("tasks")

answerDoc.packages.append(Package('babel', options=["russian"]))
taskDoc.packages.append(Package('babel', options=["russian"]))

for i in range(len(tasks)):
    tasks[i].addTexAnswer(i + 1, answerDoc)
    tasks[i].addTexTask(taskDoc)

answerDoc.generate_tex()
taskDoc.generate_tex()

