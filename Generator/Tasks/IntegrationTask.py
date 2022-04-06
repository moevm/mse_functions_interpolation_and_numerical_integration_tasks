from numpy import random
from copy import copy
from pylatex import Document, Tabular, Package, NewLine, \
    MultiRow, Command, NewPage
from pylatex.utils import NoEscape, bold, italic
from django.conf import settings
import os

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

        if type(dotsCnt) != int:
            return None

        firstX = random.randint(-10, 10)

        h = random.choice([0.1, 0.2, 0.3])
        self.xValues = [i * h + firstX for i in range(dotsCnt)]

        self.n = dotsCnt

        half = int((dotsCnt - 2) / 2)

        self.yValues.append(round(random.uniform(-9, 9), 1))
        for i in range(1, half + 1):
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

        res = abs(self.yValues[0] + self.yValues[-1]) * h / 2
        while res > 0.2 or res == 0:
            self.yValues[-1] = round(random.uniform(-9, 9), 1)
            res = abs(self.yValues[0] + self.yValues[-1]) * h / 2

        self.answer = trapezoid(self.yValues, h)
        self.halfAnswer = trapezoid(self.yValues[::2], h * 2)

        return self

    def errorRunge(self):
        return abs(self.halfAnswer - self.answer) / 3

    def taskText(self):
        return NoEscape(r"\hspace{5mm}" + bold("1). ") + "Вычислить приближённое значение " +
                        r"$\int_{" + "{0:.1f}".format(self.xValues[0]) + "}^{" + "{0:.1f}".format(
            self.xValues[-1]) + "}f(x)dx$" \
                                r"\hspace{1mm}от таблично заданной функции по " + italic("формуле трапеций ")+ "по "
                        + d[int(self.n / 2) + self.n % 2] + " и по " + d[self.n] + " узлам." \
                         " Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")

    def answerStr(self):
        return NoEscape("$S_" + str(int(self.n / 2) + len(self.yValues) % 2) + "=" + "{0:.2f}".format(self.halfAnswer) +
                        r"\rightarrow" + "{0:.2f}".format(self.answer) + r"\rightarrow" +
                        "{0:.3f}".format(
                            self.answer + (self.answer - self.halfAnswer) / 3) + r"$\hspace{1mm}(трапеции)")


class SimpsonTask:
    def __init__(self):
        self.xValues = []
        self.yValues = []
        self.answer = 0
        self.halfAnswer = 0
        self.n = 0

    def randomize(self, dotsCnt):

        if type(dotsCnt) != int:
            return None

        firstX = random.randint(-10, 10)

        h = 0.6
        self.xValues = [i * h + firstX for i in range(dotsCnt)]

        self.n = dotsCnt

        self.yValues.append(round(random.uniform(-9, 9), 1))
        self.yValues += self.generateMiddleValues()

        self.yValues.append(round(random.uniform(-9, 9), 1))
        res = abs(self.yValues[0] + self.yValues[-1]) * h / 3
        while res > 0.2 or res == 0:
            self.yValues[-1] = round(random.uniform(-9, 9), 1)
            res = abs(self.yValues[0] + self.yValues[-1]) * h / 3

        self.answer = simpson(self.yValues, h)
        self.halfAnswer = simpson(self.yValues[::2], h * 2)

        return self

    def generateMiddleValues(self):
        values = []
        number_of_values = self.n - 2

        if number_of_values == 1:
            return [0]

        # answer_2h - answer_h = (y0 - 4*y1 + 6*y2 - 4*y3 + 2*y4 - 4*y5 + 6*y6 - 4*y7 + ... + y_last) * h/3
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
        minus_four_coefficient.append(round(-value1 + 3/2 * value2, 1))

        for i in range(int(number_of_values/2)):
            if i % 2 == 0:
                # 2*y4 - 4*y5 = 0
                # y4 = 2*y5
                value = round(random.uniform(-4.5, 4.5), 1)
                two_coefficient.append(round(value * 2, 1))             # y4
                minus_four_coefficient.append(value)                    # y5
            else:
                value = round(random.uniform(-6, 6), 1)
                if int(value * 10) % 2 == 1:
                    value = round(value + 0.1, 1)

                # 6*y6 - 4*y7 = 0
                # y7 = 3/2 * y6
                six_coefficient.append(value)                           # y6
                minus_four_coefficient.append(round(3/2 * value, 1))    # y7

        # Shuffle values to make dependency on each other less obvious
        random.shuffle(minus_four_coefficient)
        random.shuffle(two_coefficient)
        random.shuffle(six_coefficient)

        values.append(minus_four_coefficient.pop())
        values.append(six_coefficient.pop())
        values.append(minus_four_coefficient.pop())

        for i in range(int(number_of_values/2)):
            if i % 2 == 0:
                values.append(two_coefficient.pop())
                values.append(minus_four_coefficient.pop())
            else:
                values.append(six_coefficient.pop())
                values.append(minus_four_coefficient.pop())

        return values

    def errorRunge(self):
        return abs(self.halfAnswer - self.answer) / 15

    def taskText(self):
        return NoEscape( r"\hspace{5mm}" + bold('2). ') + "Вычислить приближённое значение " +
                        r"$\int_{" + "{0:.1f}".format(self.xValues[0]) + "}^{" + "{0:.1f}".format(
            self.xValues[-1]) + "}f(x)dx$" \
                                r"\hspace{1mm}от таблично заданной функции по " + italic("формуле Симпсона ")+ "по "
                        + d[int(self.n / 2) + self.n % 2] + " и по " + d[self.n] + " узлам." \
                                                                                   " Оценить погрешность по правилу Рунге; уточнить результат по Ричардсону.")

    def answerStr(self):
        return NoEscape("$S_" + str(int(self.n / 2) + len(self.yValues) % 2) + "=" + "{0:.3f}".format(self.halfAnswer) +
                        r"\rightarrow" + "{0:.3f}".format(self.answer) + r"\rightarrow" +
                        "{0:.3f}".format(
                            self.answer + (self.answer - self.halfAnswer) / 15) + r"$\hspace{1mm}(Симпсон)")


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
        table.add_row([NoEscape("$ x_i $")] + [NoEscape("${0:.1f}$".format(xValues[i])) for i in
                               range(valueStartPoint, valueStartPoint + colmsCnt)])
        table.add_hline()
        table.add_row([NoEscape("$ f_i $")] + [NoEscape("${0:.1f}$".format(yValues[i])) for i in
                               range(valueStartPoint, valueStartPoint + colmsCnt)])
        table.add_hline()

        tables.append(copy(table))
        table.clear()
        valueCnt -= colmsCnt
        valueStartPoint += colmsCnt

    tableView = "|l|"
    tableView += "l|" * valueCnt

    table = Tabular(tableView)
    table.add_hline()
    table.add_row(
        [NoEscape("$ x_i $")] + [NoEscape("${0:.1f}$".format(xValues[i])) for i in range(valueStartPoint, valueStartPoint + valueCnt)])
    table.add_hline()
    table.add_row(
        [NoEscape("$ f_i $")] + [NoEscape("${0:.1f}$".format(yValues[i])) for i in range(valueStartPoint, valueStartPoint + valueCnt)])
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


def createDocs(answerDoc, taskDoc, taskCnt, trapezoidTasks, simpsonTasks, surnames, seed):
    seedStr = "({0})".format(seed)

    trapezoidTasks.append(None)
    simpsonTasks.append(None)

    if surnames is not None:
        surnames.append(None)

    table = Tabular("p{9cm}p{9cm}")

    addedVariantsCnt = 0
    for i in range(0, taskCnt, 2):
        addEmptySpace(table, 1)
        if surnames is None:
            table.add_row([NoEscape(bold("Вариант {0} ".format(i + 1)) + seedStr), "" if i + 1 == taskCnt else NoEscape(bold("Вариант {0} ".format(i + 2)) + seedStr)])
        else:
            table.add_row([surnames[i] +" " +seedStr, "" if surnames[i + 1] is None else surnames[i + 1] +" "+ seedStr])

        addEmptySpace(table, 1)

        table.add_row(trapezoidTasks[i].taskText(),
                      "" if trapezoidTasks[i + 1] is None else trapezoidTasks[i + 1].taskText())
        fillTaskTables(table, trapezoidTasks[i], trapezoidTasks[i + 1])
        addEmptySpace(table, 2)

        table.add_row(simpsonTasks[i].taskText(), "" if simpsonTasks[i + 1] is None else simpsonTasks[i + 1].taskText())
        fillTaskTables(table, simpsonTasks[i], simpsonTasks[i + 1])
        addEmptySpace(table, 3)

        addedVariantsCnt += 2

        if addedVariantsCnt == 4 and i + 2 < taskCnt:
            addedVariantsCnt = 0
            taskDoc.append(copy(table))
            taskDoc.append(NewPage())
            table.clear()
        
    taskDoc.append(table)

    answerTable = Tabular(" |p{9cm}|p{9cm}| ")
    answerTable.add_hline()

    addedVariantsCnt = 0
    for i in range(0, taskCnt, 2):
        addEmptySpace(answerTable, 1)
        if surnames is None:
            answerTable.add_row([bold("Вариант {0} ".format(i + 1) + seedStr), "" if i + 1 == taskCnt else bold("Вариант {0} ".format(i + 2) + seedStr)])
        else:
            answerTable.add_row([surnames[i] + seedStr, "" if surnames[i + 1] is None else surnames[i + 1] + seedStr])

        addEmptySpace(answerTable, 1)

        fillTaskTables(answerTable, trapezoidTasks[i], trapezoidTasks[i + 1])
        addEmptySpace(answerTable, 2)

        answerTable.add_row(trapezoidTasks[i].answerStr(),
                            "" if i + 1 == taskCnt else trapezoidTasks[i + 1].answerStr())
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

    taskDoc = Document("tasks", geometry_options={"lmargin": "3mm", "tmargin": "3mm"},
                       documentclass=Command('documentclass', options=['a4paper'], arguments=['article']),
                       page_numbers=False)
    
    answerDoc.packages.append(Package('babel', options=["russian"]))
    answerDoc.packages.append(Package('tempora'))
    taskDoc.packages.append(Package('babel', options=["russian"]))
    taskDoc.packages.append(Package('tempora'))
    return answerDoc, taskDoc


async def run(taskCnt, trapezoidsDotsCnt, simpsonDotsCnt, fileName, is_pdf, is_latex, timestamp, seed, surnames=None):
    if seed is None:
        seed = random.randint(0, 1000000)
    random.seed(seed)

    simpsonTasks = [SimpsonTask().randomize(trapezoidsDotsCnt) for i in range(taskCnt)]
    trapezoidTasks = [TrapezoidTask().randomize(simpsonDotsCnt) for j in range(taskCnt)]

    answerDoc, taskDoc = initDocs()
    createDocs(answerDoc, taskDoc, taskCnt, trapezoidTasks, simpsonTasks, surnames, seed)

    folder = os.path.join(
        settings.BASE_DIR,
        'generator',
        'static',
        'generator',
        'variants',
        timestamp
    )
    #    folder = f'generator/static/generator/{timestamp}'
    if is_pdf:
        taskDoc.generate_pdf(f'{folder}/integration_{fileName}')
        answerDoc.generate_pdf(f'{folder}/integration_answers_for_{fileName}')
    if is_latex:
        taskDoc.generate_tex(f'{folder}/integration_{fileName}')
        answerDoc.generate_tex(f'{folder}/integration_answers_for_{fileName}')
