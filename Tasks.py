from pylatex import Document, Section, NewPage, Command, Package, UnsafeCommand, Center, Tabular, MultiRow
from pylatex.base_classes import CommandBase, Arguments
from Polynomial import Polynomial
import math


class tasktext(CommandBase):
    _latex_name = 'tasktext'


class Tasks:
    def __init__(self, options_summary: int, options_in_line: int, degree: int):
        self.options_summary = options_summary
        self.options_in_line = options_in_line
        self.degree = degree
        self.doc = Document(documentclass=Command('documentclass', options=['a4paper'], arguments=['article']))
        self.doc.packages.add(Package('grffile', options=['encoding', 'filenameencoding=utf8']))
        self.doc.packages.append(
            Package('geometry', options=["textwidth=20cm", "textheight=28cm", "margin=0.3cm", "includefoot=True"]))
        self.doc.packages.append(Package('fontenc', options=["T2A"]))
        self.doc.packages.append(Package('inputenc', options=["utf8"]))
        self.doc.packages.append(Package('babel', options=["russian"]))
        self.doc.packages.append(Package('array'))
        self.doc.packages.append(Package('multirow'))
        self.doc.packages.append(Package('underscore'))
        self.doc.packages.append(Package('longtable'))
        self.doc.packages.append(Package('lastpage'))

        text_variant = r'Вариант {#1}.\newline Построить интерполяционный многочлен в форме Лагранжа, в форме Ньютона и сравнить результаты.'
        self.doc.append(UnsafeCommand('newcommand', r'\tasktext', options=1, extra_arguments=text_variant))

    def __section(self, x: list, y: list):
        table = Tabular(table_spec='c'.join(["|" for _ in range(self.degree + 3)]))
        table.add_hline()
        table.add_row(['$x_i$'] + x, escape=False)
        table.add_hline()
        table.add_row(['$y_i$'] + y, escape=False)
        table.add_hline()
        center = Center()
        center.append(table)
        return center

    def generate(self):
        quantity_of_variants_on_one_page = self.options_in_line * 6  # 6 rows in one page
        quantity_of_pages = math.ceil(self.options_summary / quantity_of_variants_on_one_page)
        column_size = 18 // self.options_in_line  # 18cm - width of a4 format

        for page in range(quantity_of_pages):
            # большая таблица на всю страницу состоящая либо из 2х либо из 3х столбцов
            table = Tabular('c'.join(['|' for _ in range(self.options_in_line + 1)]))
            table.add_hline()

            for i in range(6):
                variants = []
                for j in range(self.options_in_line):
                    variants.append(Polynomial(self.degree))
                row = []

                for j in range(self.options_in_line):
                    # смотрим не выходит ли текущий индекс за последний индекс, если да: создаём ячейку без данных
                    if page*quantity_of_variants_on_one_page + i*self.options_in_line + j > self.options_summary - 1:
                        row.append(MultiRow(5, width=f'{column_size}cm'))
                    else:
                        row.append(MultiRow(5, width=f'{column_size}cm', data=tasktext(
                            arguments=Arguments(page*quantity_of_variants_on_one_page + i*self.options_in_line + j))))
                table.add_row(row)
                row.clear()
                table = self.suplement_table(table)

                for j in range(self.options_in_line):
                    # смотрим не выходит ли текущий индекс за последний индекс, если да: создаём ячейку без данных
                    if page*quantity_of_variants_on_one_page + i*self.options_in_line + j > self.options_summary - 1:
                        row.append(MultiRow(5, width=f'{column_size}cm'))
                    else:
                        row.append(MultiRow(5, width=f'{column_size}cm', data=self.__section(variants[j].x, variants[j].y)))
                table.add_row(row)
                row.clear()
                table = self.suplement_table(table)
                table.add_hline()

                # если последний_индекс_в_текущей_строке >= нужному количеству вариантов
                if page*quantity_of_variants_on_one_page + i*self.options_in_line + self.options_in_line - 1 >= self.options_summary - 1:
                    break
            self.doc.append(table)
            self.doc.append(NewPage())
        self.doc.generate_pdf('file')
        self.doc.generate_tex("file")

    def suplement_table(self, table):
        for i in range(4):
            table.add_empty_row()
        return table
