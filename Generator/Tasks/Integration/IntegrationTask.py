from copy import copy
from pylatex import Tabular, Center
from pylatex.utils import NoEscape


class IntegrationTask:
    def __init__(self):
        self.xValues = []
        self.yValues = []
        self.answer = 0
        self.halfAnswer = 0
        self.n = 0

    def taskText(self, task_number):
        pass

    def answerStr(self):
        pass

    def errorRunge(self):
        pass

    def createTables(self):
        values_left = len(self.xValues)
        current_point = 0
        tables = []
        collums_to_fill = 6

        while values_left > 0:
            values_to_fill = min(collums_to_fill, values_left)
            table_spec = "|l|"
            table_spec += "l|" * values_to_fill

            table = Tabular(table_spec)
            table.add_hline()
            table.add_row(
                [NoEscape("$ x_i $")] + [NoEscape("${0:.1f}$".format(self.xValues[i])) for i in
                                         range(current_point,
                                               min(current_point + collums_to_fill,
                                                   len(self.xValues)))])
            table.add_hline()
            table.add_row(
                [NoEscape("$ f_i $")] + [NoEscape("${0:.1f}$".format(self.yValues[i])) for i in
                                         range(current_point,
                                               min(current_point + collums_to_fill,
                                                   len(self.xValues)))])
            table.add_hline()

            tables.append(copy(table))
            table.clear()
            values_left -= collums_to_fill
            current_point += collums_to_fill

        return tables

    def get_tex_text(self, task_number):
        main_table = Tabular("p{9cm}")
        task_text = self.taskText(task_number)
        sub_table = Tabular("p{9cm}")
        sub_table.append(task_text)
        main_table.add_row(sub_table)
        main_table.add_empty_row()
        tables = self.createTables()
        for table in tables:
            center = Center()
            center.append(table)
            main_table.add_row(center)
            main_table.add_empty_row()

        return main_table

    def get_tex_answer(self, task_number):
        answer_table = Tabular("p{9cm}")
        answer_table.append(NoEscape(f'Ответ для {task_number}-го номера:\\newline'))

        # Add tables
        tables = self.createTables()
        for table in tables:
            center = Center()
            center.append(table)
            answer_table.add_row(center)
            answer_table.add_empty_row()

        answer_table.append(self.answerStr())
        answer_table.add_empty_row()
        answer_table.append("Err = " + "{0:.4f}".format(self.errorRunge()))

        return answer_table
