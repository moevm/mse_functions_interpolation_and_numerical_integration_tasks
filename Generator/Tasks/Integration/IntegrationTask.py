from copy import copy
from pylatex import Tabular, Center
from pylatex.utils import NoEscape


class IntegrationTask:
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
        self.answer = 0
        self.halfAnswer = 0
        self.n = 0

    def task_text(self, task_number):
        pass

    def answer_str(self):
        pass

    def error_runge(self):
        pass

    def createTables(self):
        values_left = len(self.x_values)
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
                [NoEscape("$ x_i $")] + [NoEscape("${0:.1f}$".format(self.x_values[i])) for i in
                                         range(current_point,
                                               min(current_point + collums_to_fill,
                                                   len(self.x_values)))])
            table.add_hline()
            table.add_row(
                [NoEscape("$ f_i $")] + [NoEscape("${0:.1f}$".format(self.y_values[i])) for i in
                                         range(current_point,
                                               min(current_point + collums_to_fill,
                                                   len(self.x_values)))])

            table.add_hline()

            tables.append(copy(table))
            table.clear()
            values_left -= collums_to_fill
            current_point += collums_to_fill

        return tables

    def get_tex_text(self, task_number):
        main_table = Tabular("p{9cm}")
        task_text = self.task_text(task_number)
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

        answer_table.append(self.answer_str())
        answer_table.add_empty_row()
        answer_table.append("Err = " + "{0:.4f}".format(self.error_runge()))

        return answer_table
