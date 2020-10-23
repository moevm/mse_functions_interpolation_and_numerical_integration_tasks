from pylatex import Document, NewPage, Command, Package, UnsafeCommand, Center, Tabular, MultiRow
from pylatex.base_classes import CommandBase, Arguments
from interpolation.Polynomial import Polynomial
from pylatex.utils import NoEscape
import math


class tasktext(CommandBase):
    _latex_name = 'tasktext'


class answertext(CommandBase):
    _latex_name = 'answertext'


class Tasks:
    def __init__(self, options_summary: int, options_in_line: int, degree: int):
        self.options_summary = options_summary
        self.options_in_line = options_in_line
        self.degree = degree
        self.tasks = Document(documentclass=Command('documentclass', options=['a4paper'], arguments=['article']))
        self.answers = Document(documentclass=Command('documentclass', options=['a4paper'], arguments=['article']))
        documents = [self.tasks, self.answers]
        for document in documents:
            document.packages.add(Package('grffile', options=['encoding', 'filenameencoding=utf8']))
            document.packages.append(
                Package('geometry', options=["textwidth=20cm", "textheight=28cm", "margin=0.3cm", "includefoot=True"]))
            document.packages.append(Package('fontenc', options=["T2A"]))
            document.packages.append(Package('inputenc', options=["utf8"]))
            document.packages.append(Package('babel', options=["russian"]))
            document.packages.append(Package('array'))
            document.packages.append(Package('multirow'))
            document.packages.append(Package('underscore'))
            document.packages.append(Package('longtable'))
            document.packages.append(Package('lastpage'))

            text_variant = r'Вариант {#1}.\newline Построить интерполяционный многочлен в форме Лагранжа, в форме Ньютона и сравнить результаты.'
            answer_variant = r'Ответ для варианта {#1}:'
            document.append(UnsafeCommand('newcommand', r'\tasktext', options=1, extra_arguments=text_variant))
            document.append(UnsafeCommand('newcommand', r'\answertext', options=1, extra_arguments=answer_variant))

    def generate_task_table(self, x: list, y: list):
        table = Tabular(table_spec='c'.join(["|" for _ in range(self.degree + 3)]))
        table.add_hline()
        table.add_row(['$x_i$'] + x, escape=False)
        table.add_hline()
        table.add_row(['$y_i$'] + y, escape=False)
        table.add_hline()
        center = Center()
        center.append(table)
        return center

    def generate_answer_table(self, coefficients):
        center = Center()
        result = ''
        for i, coefficient in enumerate(coefficients):
            if coefficient != 0:
                if i == 0:
                    result += f"{coefficient}"
                elif i == 1:
                    if coefficient != 1:
                        result += f"{coefficient}x"
                    else:
                        result += "x"
                else:
                    if coefficient != 1:
                        result += f"{coefficient}$x^{i}$"
                    else:
                        result += f"$x^{i}$"

            if i != len(coefficients) - 1:
                if coefficients[i+1] > 0:
                    result += "+"

        center.append(NoEscape(result))
        return center

    def generate(self):
        quantity_of_variants_on_one_page = self.options_in_line * 6  # 6 rows in one page
        quantity_of_pages = math.ceil(self.options_summary / quantity_of_variants_on_one_page)
        column_size = 18 // self.options_in_line  # 18cm - width of a4 format

        for page in range(quantity_of_pages):
            # большая таблица на всю страницу состоящая либо из 2х либо из 3х столбцов
            tasks_table = Tabular('c'.join(['|' for _ in range(self.options_in_line + 1)]))
            answers_table = Tabular('c'.join(['|' for _ in range(self.options_in_line + 1)]))
            tasks_table.add_hline()
            answers_table.add_hline()

            for i in range(6):
                variants = []
                answers = []
                for j in range(self.options_in_line):
                    polynom = Polynomial(self.degree)
                    variants.append(polynom)
                    answers.append(polynom)
                tasks_row = []
                answers_row = []

                for j in range(self.options_in_line):
                    # смотрим не выходит ли текущий индекс за последний индекс, если да: создаём ячейку без данных
                    if page*quantity_of_variants_on_one_page + i*self.options_in_line + j > self.options_summary - 1:
                        tasks_row.append(MultiRow(5, width=f'{column_size}cm'))
                        answers_row.append(MultiRow(5, width=f'{column_size}cm'))
                    else:
                        tasks_row.append(MultiRow(5, width=f'{column_size}cm', data=tasktext(
                            arguments=Arguments(page*quantity_of_variants_on_one_page + i*self.options_in_line + j))))
                        answers_row.append(MultiRow(5, width=f'{column_size}cm', data=answertext(
                            arguments=Arguments(page*quantity_of_variants_on_one_page + i*self.options_in_line + j))))
                        print(f"Вариант {page * quantity_of_variants_on_one_page + i * self.options_in_line + j}, полином: {variants[j].coefficients}")

                tasks_table.add_row(tasks_row)
                answers_table.add_row(answers_row)
                answers_table = self.suplement_table(answers_table, n=2)

                tasks_row.clear()
                answers_row.clear()

                tasks_table = self.suplement_table(tasks_table)

                for j in range(self.options_in_line):
                    # смотрим не выходит ли текущий индекс за последний индекс, если да: создаём ячейку без данных
                    if page*quantity_of_variants_on_one_page + i*self.options_in_line + j > self.options_summary - 1:
                        tasks_row.append(MultiRow(5, width=f'{column_size}cm'))
                        answers_row.append(MultiRow(5, width=f'{column_size}cm'))
                    else:
                        tasks_row.append(MultiRow(5, width=f'{column_size}cm', data=self.generate_task_table(variants[j].x, variants[j].y)))
                        answers_row.append(MultiRow(5, width=f'{column_size}cm', data=self.generate_answer_table(answers[j].coefficients)))
                tasks_table.add_row(tasks_row)
                answers_table.add_row(tasks_row)
                answers_table = self.suplement_table(answers_table, n=2)
                answers_table.add_row(answers_row)

                tasks_row.clear()
                answers_row.clear()

                tasks_table = self.suplement_table(tasks_table)
                answers_table = self.suplement_table(answers_table)

                tasks_table.add_hline()
                answers_table.add_hline()

                # если последний_индекс_в_текущей_строке >= нужному количеству вариантов
                if page*quantity_of_variants_on_one_page + i*self.options_in_line + self.options_in_line - 1 >= self.options_summary - 1:
                    break
            self.tasks.append(tasks_table)
            self.answers.append(answers_table)

            self.tasks.append(NewPage())
            self.answers.append(NewPage())

        self.tasks.generate_pdf('examples/tasks')
        self.tasks.generate_tex('examples/tasks')
        self.answers.generate_pdf('examples/answers')
        self.answers.generate_tex('examples/answers')

    def suplement_table(self, table, n=4):
        for i in range(n):
            table.add_empty_row()
        return table
