from pylatex import Document, Command, Package, LongTable, Tabular
from pylatex.utils import NoEscape, bold
from django.conf import settings
import os


class SplineDocument:
    def __init__(self, task_list, seed):
        self.seed = seed
        self.tasks = Document(
            documentclass=Command('documentclass', options=['a4paper'], arguments=['article']),
            font_size="large")  # , ))
        self.answers = Document(
            documentclass=Command('documentclass', options=['a4paper'], arguments=['article']))
        documents = [self.tasks, self.answers]
        for document in documents:
            document.packages.add(Package('grffile', options=['encoding', 'filenameencoding=utf8']))
            document.packages.append(
                Package('geometry', options=["textwidth=20cm", "textheight=28cm", "margin=0.3cm",
                                             "includefoot=True"]))
            document.packages.append(Package('fontenc', options=["T2A"]))
            document.packages.append(Package('inputenc', options=["utf8"]))
            document.packages.append(Package('babel', options=["russian"]))
            document.packages.append(Package('tempora'))
            document.packages.append(Package('array'))
            document.packages.append(Package('multirow'))
            document.packages.append(Package('underscore'))
            document.packages.append(Package('longtable'))
            document.packages.append(Package('lastpage'))
            document.packages.append(Package('amsmath'))

        task_table = LongTable("p{9.5cm}p{9.5cm}")
        answer_table = LongTable("p{9.5cm}p{9.5cm}")
        for i in range(1, len(task_list), 2):
            task1 = task_list[i - 1]
            task2 = task_list[i]
            # Add variant and task text
            subtable1 = Tabular("p{9.5cm}")
            subtable2 = Tabular("p{9.5cm}")
            subtable1.add_row([NoEscape(bold(f'Вариант {i} ') + f'({seed})')])
            subtable2.add_row([NoEscape(bold(f'Вариант {i + 1} ') + f'({seed})')])
            subtable1.add_row([task1.get_tex_text()])
            subtable2.add_row([task2.get_tex_text()])

            task_table.add_row([subtable1, subtable2])

            # Add answer text
            answer_table.add_row([task1.get_tex_answer(i, seed), task2.get_tex_answer(i + 1, seed)])

            if i != len(task_list) - 1:
                task_table.add_empty_row()
                answer_table.add_empty_row()

        if len(task_list) % 2 == 1:
            last_task = task_list[-1]
            # Add variant and task text
            task_table.add_row([NoEscape(bold(f'Вариант {len(task_list)} ')
                                         + f'({seed})'), ""])
            task_table.add_row([last_task.get_tex_text(), ""])
            answer_table.add_row([last_task.get_tex_answer(len(task_list), seed), ""])

        self.tasks.append(task_table)
        self.answers.append(answer_table)

    async def generate(self, filename, is_pdf, is_latex, timestamp, surnames=None):
        folder = os.path.join(
            settings.BASE_DIR,
            'generator',
            'static',
            'generator',
            'variants',
            timestamp
        )
        #       folder = f'generator/static/generator/{timestamp}'
        if is_pdf:
            self.tasks.generate_pdf(f'{folder}/splines_{filename}')
            self.answers.generate_pdf(f'{folder}/splines_answers_for_{filename}')
        if is_latex:
            self.tasks.generate_tex(f'{folder}/splines_{filename}')
            self.answers.generate_tex(f'{folder}/splines_answers_for_{filename}')