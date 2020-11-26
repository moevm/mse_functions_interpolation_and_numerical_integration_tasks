from random import randint
from random import choice
from copy import copy
from pylatex import Document, Tabular, Package, NewLine, \
    MultiRow, Command, NewPage
from pylatex.utils import NoEscape

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


class TrapezoidTask:
    def __init__(self):
        self.xValues = []
        self.yValues = []
        self.answer = 0
        self.halfAnswer = 0
        self.n = 0

    def randomize(self, dotsCnt):
        firstX = randint(-10, 10)

        h = choice([0.1, 0.2, 0.3])
        self.xValues = [i * h + firstX for i in range(dotsCnt)]

        self.n = dotsCnt

        self.yValues.append(randint(-10, 10))
        for i in range(1, dotsCnt):
            self.yValues.append(self.yValues[i - 1] + randint(-dotsCnt - 2 + i, dotsCnt + 2 - i))

        if (self.yValues[-1] + self.yValues[0]) % 2 != 0:
            self.yValues[-1] -= 1

        self.answer = trapezoid(self.yValues, h)
        self.halfAnswer = trapezoid(self.yValues[::2], h)

        return self

    def errorRunge(self):
        return abs(self.halfAnswer - self.answer) / 3

    def taskText(self):
        return NoEscape("1) Вычислить приближённое значение " +
                        r"$\int_{" + "{0:.1f}".format(self.xValues[0]) + "}^{" + "{0:.1f}".format(self.xValues[-1]) + "}f(x)dx$" \
                        r"\hspace{1mm}от таблично заданной функции по формуле трапеций по "
                        + d[int(self.n / 2) + self.n % 2] + " и по " + d[self.n] + " узлам." \
                        "Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")

    def answerStr(self):
        return NoEscape("$S_" + str(int(self.n / 2) + len(self.yValues) % 2) + "=" + "{0:.2f}".format(self.halfAnswer) +
                        r"\rightarrow" + "{0:.2f}".format(self.answer) + r"\rightarrow" +
                        "{0:.3f}".format(self.answer + self.errorRunge()) + r"$\hspace{1mm}(трапеции)")


class SimpsonTask:
    def __init__(self):
        self.xValues = []
        self.yValues = []
        self.answer = 0
        self.halfAnswer = 0
        self.n = 0

    def randomize(self, dotsCnt):
        firstX = randint(-10, 10)

        h = 0.6
        self.xValues = [i * h + firstX for i in range(dotsCnt)]

        self.n = dotsCnt

        self.yValues.append(randint(-10, 10))
        for i in range(1, dotsCnt):
            self.yValues.append(self.yValues[i - 1] + randint(-dotsCnt - 2 + i, dotsCnt + 2 - i))

        if (self.yValues[-1] + self.yValues[0]) % 2 != 0:
            self.yValues[-1] -= 1

        self.answer = simpson(self.yValues, h)
        self.halfAnswer = simpson(self.yValues[::2], h)

        return self

    def errorRunge(self):
        return abs(self.halfAnswer - self.answer) / 15

    def taskText(self):
        return NoEscape("1) Вычислить приближённое значение " +
                        r"$\int_{" + "{0:.1f}".format(self.xValues[0]) + "}^{" + "{0:.1f}".format(self.xValues[-1]) + "}f(x)dx$" \
                        r"\hspace{1mm}от таблично заданной функции по формуле Симпсона по "
                        + d[int(self.n / 2) + self.n % 2] + " и по " + d[self.n] + " узлам." \
                        " Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")

    def answerStr(self):
        return NoEscape("$S_" + str(int(self.n / 2) + len(self.yValues) % 2) + "=" + "{0:.3f}".format(self.halfAnswer) +
                        r"\rightarrow" + "{0:.3f}".format(self.answer) + r"\rightarrow" +
                        "{0:.3f}".format(self.answer + self.errorRunge()) + r"$\hspace{1mm}(Симпсон)")


def simpson(y, h):
    res = y[0] + y[-1]

    for i in range(1, len(y) - 1):
        res += 4 * y[i] if i % 2 == 1 else 2 * y[i]

    res *= h / 3

    return res


def trapezoid(y, h):
    res = (y[0] + y[-1]) / 2

    for i in range(1, len(y) - 1):
        res += y[i]

    res *= h

    return res


def createTables(xValues, yValues):
    valueCnt = len(xValues)
    valueStartPoint = 0
    tables = []
    colmsCnt = 7

    while valueCnt > 7:
        tableView = "|l|"
        tableView += "l|" * colmsCnt

        table = Tabular(tableView)
        table.add_hline()
        table.add_row(["x"] + ["{0:.1f}".format(xValues[i]) for i in range(valueStartPoint, valueStartPoint + colmsCnt)])
        table.add_hline()
        table.add_row(["y"] + ["{0:.1f}".format(yValues[i]) for i in range(valueStartPoint, valueStartPoint + colmsCnt)])
        table.add_hline()

        tables.append(copy(table))
        table.clear()
        valueCnt -= colmsCnt
        valueStartPoint += colmsCnt

    tableView = "|l|"
    tableView += "l|" * valueCnt

    table = Tabular(tableView)
    table.add_hline()
    table.add_row(["x"] + ["{0:.1f}".format(xValues[i]) for i in range(valueStartPoint, valueStartPoint + valueCnt)])
    table.add_hline()
    table.add_row(["y"] + ["{0:.1f}".format(yValues[i]) for i in range(valueStartPoint, valueStartPoint + valueCnt)])
    table.add_hline()

    tables.append(table)

    return tables


def fillTaskTables(table, firstTask, secondTask):
    firstTables = createTables(firstTask.xValues,
                               firstTask.yValues)
    secondTables = [] if secondTask is None else createTables(secondTask.xValues,
                                                              secondTask.yValues)
    for j in range(len(firstTables)):
        table.add_row(MultiRow(5, data=firstTables[j]),
                      MultiRow(5, data=secondTables[j] if secondTables else ""))
        addEmptySpace(table, 2)


def createDocs(answerDoc, taskDoc, taskCnt, trapezoidTasks, simpsonTasks, surnames=None):
    trapezoidTasks.append(None)
    simpsonTasks.append(None)

    if surnames is not None:
        surnames.append(None)

    table = Tabular(" |p{9cm}|p{9cm}| ")
    table.add_hline()

    addedVariantsCnt = 0
    for i in range(0, taskCnt, 2):
        addEmptySpace(table, 1)
        if surnames is None:
            table.add_row(["Вариант {0}".format(i + 1), "" if i + 1 == taskCnt else "Вариант {0}".format(i + 2)])
        else:
            table.add_row([surnames[i], "" if surnames[i + 1] is None else surnames[i + 1]])

        addEmptySpace(table, 1)

        table.add_row(trapezoidTasks[i].taskText(), "" if trapezoidTasks[i + 1] is None else trapezoidTasks[i + 1].taskText())
        fillTaskTables(table, trapezoidTasks[i], trapezoidTasks[i + 1])
        addEmptySpace(table, 2)

        table.add_row(simpsonTasks[i].taskText(),  "" if simpsonTasks[i + 1] is None else simpsonTasks[i + 1].taskText())
        fillTaskTables(table, simpsonTasks[i], simpsonTasks[i + 1])
        addEmptySpace(table, 3)

        addedVariantsCnt += 2

        if addedVariantsCnt == 4 and i + 2 < taskCnt:
            addedVariantsCnt = 0
            table.add_hline()
            taskDoc.append(copy(table))
            taskDoc.append(NewPage())
            table.clear()
        table.add_hline()

    taskDoc.append(table)

    answerTable = Tabular(" |p{9cm}|p{9cm}| ")
    answerTable.add_hline()

    addedVariantsCnt = 0
    for i in range(0, taskCnt, 2):
        addEmptySpace(answerTable, 1)
        if surnames is None:
            answerTable.add_row(["Вариант {0}".format(i + 1), "" if i + 1 == taskCnt else "Вариант {0}".format(i + 2)])
        else:
            answerTable.add_row([surnames[i], "" if surnames[i + 1] is None else surnames[i + 1]])

        addEmptySpace(answerTable, 1)

        fillTaskTables(answerTable, trapezoidTasks[i], trapezoidTasks[i + 1])
        addEmptySpace(answerTable, 2)

        answerTable.add_row(trapezoidTasks[i].answerStr(), "" if i + 1 == taskCnt else trapezoidTasks[i + 1].answerStr())
        addEmptySpace(answerTable, 1)
        answerTable.add_row("Err = " + "{0:.4f}".format(trapezoidTasks[i].errorRunge()),
                            "" if i + 1 == taskCnt else "Err = " + "{0:.4f}".format(trapezoidTasks[i + 1].errorRunge()))

        fillTaskTables(answerTable, simpsonTasks[i], simpsonTasks[i + 1])
        addEmptySpace(answerTable, 2)

        answerTable.add_row(simpsonTasks[i].answerStr(),
                            "" if i + 1 == taskCnt else simpsonTasks[i + 1].answerStr())
        addEmptySpace(answerTable, 1)
        answerTable.add_row("Err = " + "{0:.4f}".format(simpsonTasks[i].errorRunge()),
                            "" if i + 1 == taskCnt else "Err = " + "{0:.4f}".format(simpsonTasks[i + 1].errorRunge()))
        addEmptySpace(answerTable, 2)

        addedVariantsCnt += 2
        if addedVariantsCnt == 4 and i + 2 < taskCnt:
            addedVariantsCnt = 0
            answerTable.add_hline()
            answerDoc.append(copy(answerTable))
            answerDoc.append(NewPage())
            answerTable.clear()
        answerTable.add_hline()

    answerDoc.append(answerTable)


def addEmptySpace(table, cnt):
    for i in range(cnt):
        table.add_empty_row()


def initDocs():
    answerDoc = Document("answers", geometry_options={"lmargin": "1cm", "tmargin": "1cm"},
                         documentclass=Command('documentclass', options=['a4paper'], arguments=['article']),
                         page_numbers=False)

    taskDoc = Document("tasks", geometry_options={"lmargin": "1cm", "tmargin": "1cm"},
                       documentclass=Command('documentclass', options=['a4paper'], arguments=['article']),
                       page_numbers=False)

    answerDoc.packages.append(Package('babel', options=["russian"]))
    taskDoc.packages.append(Package('babel', options=["russian"]))

    return answerDoc, taskDoc


async def run(taskCnt, trapezoidsDotsCnt, simpsonDotsCnt, fileName, is_pdf, is_latex, timestamp, surnames=None):
    simpsonTasks = [SimpsonTask().randomize(trapezoidsDotsCnt) for i in range(taskCnt)]
    trapezoidTasks = [TrapezoidTask().randomize(simpsonDotsCnt) for j in range(taskCnt)]

    answerDoc, taskDoc = initDocs()
    createDocs(answerDoc, taskDoc, taskCnt, trapezoidTasks, simpsonTasks, surnames)

    folder = f'interpolation_integration_generator/static/interpolation_integration_generator/{timestamp}'
    if is_pdf:
        taskDoc.generate_pdf(f'{folder}/integration_{fileName}')
        answerDoc.generate_pdf(f'{folder}/integration_answers_for_{fileName}')
    if is_latex:
        taskDoc.generate_tex(f'{folder}/integration_{fileName}')
        answerDoc.generate_tex(f'{folder}/integration_answers_for_{fileName}')
