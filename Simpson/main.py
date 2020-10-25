from random import randint
from random import choice
from copy import copy
from pylatex import Document, Tabular, Package, NewLine, \
    MultiRow, Command, NewPage
from pylatex.utils import NoEscape


class TrapezoidTask:
    def __init__(self):
        self.xValues = []
        self.yValues = []
        self.answer = 0
        self.n = 0

    def randomize(self, dotsCnt):
        self.n = choice([5, 10])

        a = randint(0, 3)
        self.xValues = [a + i * (1 / self.n) for i in range(dotsCnt)]
        while True:
            self.yValues = [randint(-20, 20) for i in range(dotsCnt)]
            if (self.yValues[0] + self.yValues[-1]) % 2 == 1:
                self.yValues[-1] += 1

            self.answer = trapezoid(self.yValues, self.xValues[0], self.xValues[-1], self.n)
            if 30 > abs(self.answer) >= 1:
                return self

    def errorRunge(self):
        return abs(simpson(self.yValues, self.xValues[0], self.xValues[-1], self.n) -
                   simpson(self.yValues, self.xValues[0], self.xValues[-1], self.n * 2)) / 3

    def addTexAnswer(self, answerDoc):
        answerDoc.append(NoEscape("1) Ответ: {0}, погрешность: {1}".format("{0:.1f}".format(self.answer),
                                                                           "{0:.4f}".format(self.errorRunge()))))
        answerDoc.append(NewLine())

    def taskText(self):
        return "1) Метод Трапеций"

    def valueTable(self):
        tableView = "|c|"
        tableView += "c|" * len(self.xValues)

        table = Tabular(tableView)
        table.add_hline()
        table.add_row(["x"] + ["{0:.1f}".format(i) for i in self.xValues])
        table.add_hline()
        table.add_row(["y"] + self.yValues)
        table.add_hline()

        return table


class SimpsonTask:
    def __init__(self):
        self.xValues = []
        self.yValues = []
        self.answer = 0
        self.n = 0

    def randomize(self, dotsCnt):
        self.n = choice([5, 10])

        a = randint(0, 3)
        self.xValues = [a + i * (1 / self.n) for i in range(dotsCnt)]
        while True:
            self.__generateYValues(dotsCnt)
            if 30 > abs(self.answer) >= 1:
                return self

    def __generateYValues(self, dotsCnt):
        self.yValues = [randint(-20, 20) for i in range(dotsCnt)]

        res = self.yValues[0]
        for i in range(1, len(self.yValues) - 1):
            if i % 2 == 1:
                res += 4 * self.yValues[i]
            else:
                res += 2 * self.yValues[i]

        resDenominator = self.n * 3

        self.yValues[-1] = resDenominator - res % resDenominator
        res += self.yValues[-1]

        res /= resDenominator
        res *= (self.xValues[-1] - self.xValues[0])
        self.answer = res

    def errorRunge(self):
        return abs(simpson(self.yValues, self.xValues[0], self.xValues[-1], self.n) -
                   simpson(self.yValues, self.xValues[0], self.xValues[-1], self.n * 2)) / 15

    def addTexAnswer(self, answerDoc):

        answerDoc.append(NoEscape(r"\hspace*{4mm}" + "2) Ответ: {0}, погрешность: "
                                                     "{1}".format("{0:.1f}".format(self.answer),
                                                                  "{0:.4f}".format(self.errorRunge()))))
        answerDoc.append(NewLine())

    def taskText(self):
        return "2) Метод Симпсона"

    def valueTable(self):
        tableView = "|c|"
        tableView += "c|" * len(self.xValues)

        table = Tabular(tableView)
        table.add_hline()
        table.add_row(["x"] + ["{0:.1f}".format(i) for i in self.xValues])
        table.add_hline()
        table.add_row(["y"] + self.yValues)
        table.add_hline()

        return table


def simpson(y, a, b, n):
    res = y[0] + y[-1]

    for i in range(1, len(y) - 1):
        if i % 2 == 1:
            res += 4 * y[i]
        else:
            res += 2 * y[i]

    res /= n * 3
    res *= (b - a)

    return res


def trapezoid(y, a, b, n):
    res = (y[0] + y[-1]) / 2

    for i in range(1, len(y) - 1):
        res += y[i]

    res /= n
    res *= (b - a)

    return res


taskCnt = 9
simpsonTasks = [SimpsonTask().randomize(9) for i in range(taskCnt)]
trapezoidTasks = [TrapezoidTask().randomize(9) for j in range(taskCnt)]

answerDoc = Document("answers", geometry_options={"lmargin": "0cm", "tmargin": "1cm"},
                     documentclass=Command('documentclass', options=['a4paper'], arguments=['article']), page_numbers=False)

taskDoc = Document("tasks", geometry_options={"lmargin": "1cm", "tmargin": "1cm"},
                   documentclass=Command('documentclass', options=['a4paper'], arguments=['article']), page_numbers=False)

answerDoc.packages.append(Package('babel', options=["russian"]))
taskDoc.packages.append(Package('babel', options=["russian"]))

table = Tabular("|c|c|")
table.add_hline()

for i in range(0, taskCnt, 2):
    if i == taskCnt - 1:
        table.add_row(["Вариант {0}".format(i), ""])
        table.add_row(trapezoidTasks[i].taskText(), "")
        table.add_row(MultiRow(5, data=trapezoidTasks[i].valueTable()),
                      MultiRow(5, width="9cm"))

        for j in range(4):
            table.add_empty_row()

        table.add_row(simpsonTasks[i].taskText(), "")
        table.add_row(MultiRow(5, data=simpsonTasks[i].valueTable()),
                      MultiRow(5, width="9cm"))
        for j in range(4):
            table.add_empty_row()
        table.add_hline()
        break

    table.add_row(["Вариант {0}".format(i), "Вариант {0}".format(i + 1)])

    table.add_row(trapezoidTasks[i].taskText(), trapezoidTasks[i + 1].taskText())
    table.add_row(MultiRow(5, width="9cm", data=trapezoidTasks[i].valueTable()),
                  MultiRow(5, width="9cm", data=trapezoidTasks[i + 1].valueTable()))

    for j in range(4):
        table.add_empty_row()

    table.add_row(simpsonTasks[i].taskText(), simpsonTasks[i + 1].taskText())
    table.add_row(MultiRow(5, width="9cm", data=simpsonTasks[i].valueTable()),
                  MultiRow(5, width="9cm", data=simpsonTasks[i + 1].valueTable()))

    for j in range(4):
        table.add_empty_row()
    table.add_hline()
    if i == 6:
        taskDoc.append(copy(table))
        taskDoc.append(NewPage())
        table.clear()
        table.add_hline()


taskDoc.append(table)


for i in range(taskCnt):
    answerDoc.append(NoEscape(r"\noindent {0}. ".format(i)))
    trapezoidTasks[i].addTexAnswer(answerDoc)
    simpsonTasks[i].addTexAnswer(answerDoc)
    answerDoc.append(NewLine())

answerDoc.generate_tex()
taskDoc.generate_tex()

