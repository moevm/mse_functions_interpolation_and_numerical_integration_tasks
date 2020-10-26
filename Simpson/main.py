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
        return NoEscape("1) Вычислить приближённое значение " +
                        r"$\int_{" + "{0:.1f}".format(self.xValues[0]) + "}^{" + "{0:.1f}".format(self.xValues[-1]) + "}f(x)dx$" \
                        r"\hspace{1mm}от таблично заданной функции по формуле трапеций по шести и по девяти узлам. " \
                        "Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")


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
        return NoEscape("2) Вычислить приближённое значение " +
                        r"$\int_{" + "{0:.1f}".format(self.xValues[0]) + "}^{" + "{0:.1f}".format(self.xValues[-1]) + "}f(x)dx$" \
                        r"\hspace{1mm}от таблично заданной функции по формуле Cимпсона по шести и по девяти узлам. " \
                        "Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")


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


def createTables(xValues, yValues):
    valueCnt = len(xValues)
    valueStartPoint = 0
    tables = []

    while valueCnt > 9:
        tableView = "|l|"
        tableView += "l|" * 9

        table = Tabular(tableView)
        table.add_hline()
        table.add_row(["x"] + ["{0:.1f}".format(xValues[i]) for i in range(valueStartPoint, valueStartPoint + 9)])
        table.add_hline()
        table.add_row(["y"] + yValues[valueStartPoint:valueStartPoint + 9:])
        table.add_hline()

        tables.append(copy(table))
        table.clear()
        valueCnt -= 9
        valueStartPoint += 9

    tableView = "|l|"
    tableView += "l|" * valueCnt

    table = Tabular(tableView)
    table.add_hline()
    table.add_row(["x"] + ["{0:.1f}".format(xValues[i]) for i in range(valueStartPoint, valueStartPoint + valueCnt)])
    table.add_hline()
    table.add_row(["y"] + yValues[valueStartPoint:valueStartPoint + valueCnt:])
    table.add_hline()

    tables.append(table)

    return tables


def fillFullTask(table, firstTask, secondTask):
    table.add_row(firstTask.taskText(), "" if secondTask is None else secondTask.taskText())

    firstTables = createTables(firstTask.xValues,
                               firstTask.yValues)
    secondTables = [] if secondTask is None else createTables(secondTask.xValues,
                                                              secondTask.yValues)
    for j in range(len(firstTables)):
        table.add_row(MultiRow(5, data=firstTables[j]),
                      MultiRow(5, data=secondTables[j] if secondTables else ""))
        addEmptySpace(table, 2)


def createDocs(answerDoc, taskDoc, taskCnt):
    simpsonTasks = [SimpsonTask().randomize(11) for i in range(taskCnt)]
    trapezoidTasks = [TrapezoidTask().randomize(11) for j in range(taskCnt)]
    trapezoidTasks.append(None)
    simpsonTasks.append(None)

    table = Tabular(" p{9cm} p{9cm} ")

    addedVariantsCnt = 0
    for i in range(0, taskCnt, 2):
        addEmptySpace(table, 1)
        table.add_row(["Вариант {0}".format(i + 1), "" if i + 1 == taskCnt else "Вариант {0}".format(i + 2)])
        addEmptySpace(table, 1)

        fillFullTask(table, trapezoidTasks[i], trapezoidTasks[i + 1])
        addEmptySpace(table, 2)
        fillFullTask(table, simpsonTasks[i], simpsonTasks[i + 1])
        addEmptySpace(table, 3)

        addedVariantsCnt += 2

        if addedVariantsCnt == 4:
            addedVariantsCnt = 0
            taskDoc.append(copy(table))
            taskDoc.append(NewPage())
            table.clear()

    taskDoc.append(table)

    answerTable = Tabular(" p{9cm} p{9cm} ")
    for i in range(0, taskCnt, 2):
        addEmptySpace(answerTable, 1)
        answerTable.add_row(["Вариант {0}".format(i + 1), "" if i + 1 == taskCnt else "Вариант {0}".format(i + 2)])
        addEmptySpace(answerTable, 1)

        answerTable.add_row("1)" + str(trapezoidTasks[i].answer), "" if i + 1 == taskCnt else "1)" + str(trapezoidTasks[i + 1].answer))
        answerTable.add_row("2)" + str(simpsonTasks[i].answer), "" if i + 1 == taskCnt else "2)" + str(simpsonTasks[i + 1].answer))
        addEmptySpace(answerTable, 1)

    answerDoc.append(answerTable)


def addEmptySpace(table, cnt):
    for i in range(cnt):
        table.add_empty_row()


taskCnt = 11

answerDoc = Document("answers", geometry_options={"lmargin": "1cm", "tmargin": "1cm"},
                     documentclass=Command('documentclass', options=['a4paper'], arguments=['article']), page_numbers=False)

taskDoc = Document("tasks", geometry_options={"lmargin": "1cm", "tmargin": "1cm"},
                   documentclass=Command('documentclass', options=['a4paper'], arguments=['article']), page_numbers=False)

answerDoc.packages.append(Package('babel', options=["russian"]))
taskDoc.packages.append(Package('babel', options=["russian"]))

createDocs(answerDoc, taskDoc, taskCnt)

answerDoc.generate_tex()
taskDoc.generate_tex()

