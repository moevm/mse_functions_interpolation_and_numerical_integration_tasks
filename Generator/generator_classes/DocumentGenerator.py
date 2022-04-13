import os
import zipfile
from os.path import basename
from pylatex import Document, Command, Package, LongTable, Tabular
from pylatex.utils import NoEscape, bold
from django.conf import settings


class DocumentGenerator:
    def __init__(self, seed, filename, timestamp, type_str='custom',
                 generate_pdf=False, generate_latex=False):
        self.seed = seed
        self.filename = filename
        self.type = type_str
        self.folder = os.path.join(
            settings.BASE_DIR,
            'generator',
            'static',
            'generator',
            'variants',
            timestamp
        )
        os.mkdir(f"{self.folder}")

        # TODO: remove?
        self.static_folder = f"/static/generator/variants/{timestamp}"

        self.generate_pdf = generate_pdf
        self.generate_latex = generate_latex

        self.tasks_document = Document(
            documentclass=Command('documentclass', options=['a4paper'], arguments=['article']),
            font_size="normalsize")
        self.answers_document = Document(
            documentclass=Command('documentclass', options=['a4paper'], arguments=['article']))

        documents = [self.tasks_document, self.answers_document]
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

    def generate_document(self, variants_list, seed):
        task_table = LongTable("p{9.5cm}p{9.5cm}")
        answer_table = LongTable("p{9.5cm}p{9.5cm}")
        length = len(variants_list[0])
        print(length)
        for j in range(1, len(variants_list), 2):
            task_list1 = variants_list[j - 1]
            task_list2 = variants_list[j]

            task_subtable1 = Tabular("p{9.5cm}")
            task_subtable2 = Tabular("p{9.5cm}")
            task_subtable1.add_row([NoEscape(bold(f'Вариант {j} ') + f'({seed})')])
            task_subtable2.add_row([NoEscape(bold(f'Вариант {j + 1} ') + f'({seed})')])

            answer_subtable1 = Tabular("p{9.5cm}")
            answer_subtable2 = Tabular("p{9.5cm}")
            answer_subtable1.add_row([NoEscape(bold(f'Вариант {j} ') + f'({seed})')])
            answer_subtable2.add_row([NoEscape(bold(f'Вариант {j + 1} ') + f'({seed})')])

            for i in range(len(task_list1)):
                task1 = task_list1[i]
                task2 = task_list2[i]

                # Add task text
                task_subtable1.add_row([task1.get_tex_text(i + 1)])
                task_subtable2.add_row([task2.get_tex_text(i + 1)])

                # Add task answer
                answer_subtable1.add_row([task1.get_tex_answer(i + 1)])
                answer_subtable2.add_row([task2.get_tex_answer(i + 1)])

                # Add empty row between tasks
                task_subtable1.add_empty_row()
                task_subtable2.add_empty_row()
                answer_subtable1.add_empty_row()
                answer_subtable2.add_empty_row()

            task_table.add_row([task_subtable1, task_subtable2])
            answer_table.add_row([answer_subtable1, answer_subtable2])

        if len(variants_list) % 2 == 1:
            last_task_list = variants_list[-1]

            task_subtable = Tabular("p{9.5cm}")
            task_subtable.add_row(
                [NoEscape(bold(f'Вариант {len(variants_list)} ') + f'({seed})')])

            answer_subtable = Tabular("p{9.5cm}")
            answer_subtable.add_row(
                [NoEscape(bold(f'Вариант {len(variants_list)} ') + f'({seed})')])

            for i in range(len(last_task_list)):
                task = last_task_list[i]
                # Add task text
                task_subtable.add_row([task.get_tex_text()])

                # Add task answer
                answer_subtable.add_row([task.get_tex_answer(i + 1)])

                # Add empty row between tasks
                task_subtable.add_empty_row()
                answer_subtable.add_empty_row()

            task_table.add_row([task_subtable, NoEscape("")])
            answer_table.add_row([answer_subtable, NoEscape("")])

        self.tasks_document.append(task_table)
        self.answers_document.append(answer_table)

        filenames = []
        names = []
        files = []
        sizes = []

        if self.generate_pdf:
            self.tasks_document.generate_pdf(f'{self.folder}/{self.type}_{self.filename}')
            self.answers_document.generate_pdf(
                f'{self.folder}/{self.type}_answers_for_{self.filename}')

            filenames.append(f"{self.folder}/{self.type}_{self.filename}.pdf")
            filenames.append(f'{self.folder}/{self.type}_answers_for_{self.filename}.pdf')

            names.append(f"{self.type}_{self.filename}.pdf")
            files.append(f"{self.static_folder}/{self.type}_{self.filename}.pdf")
            sizes.append(os.path.getsize(f"{self.folder}/{self.type}_{self.filename}.pdf"))

            names.append(f"{self.type}_answers_for_{self.filename}.pdf")
            files.append(f"{self.static_folder}/{self.type}_answers_for_{self.filename}.pdf")
            sizes.append(
                os.path.getsize(f"{self.folder}/{self.type}_answers_for_{self.filename}.pdf"))

        if self.generate_latex:
            self.tasks_document.generate_tex(f'{self.folder}/{self.type}_{self.filename}')
            self.answers_document.generate_tex(
                f'{self.folder}/{self.type}_answers_for_{self.filename}')

            filenames.append(f"{self.folder}/{self.type}_{self.filename}.tex")
            filenames.append(f'{self.folder}/{self.type}_answers_for_{self.filename}.tex')

            names.append(f"{self.type}_{self.filename}.tex")
            files.append(f"{self.static_folder}/{self.type}_{self.filename}.tex")
            sizes.append(os.path.getsize(f"{self.folder}/{self.type}_{self.filename}.tex"))

            names.append(f"{self.type}_answers_for_{self.filename}.tex")
            files.append(f"{self.static_folder}/{self.type}_answers_for_{self.filename}.tex")
            sizes.append(
                os.path.getsize(f"{self.folder}/{self.type}_answers_for_{self.filename}.tex"))

        with zipfile.ZipFile(f'{self.folder}/{self.type}_result.zip', 'w') as zipObj:
            for file in filenames:
                zipObj.write(file, basename(file))

        names.append(f"{self.type}_result.zip")
        files.append(f"{self.static_folder}/{self.type}_result.zip")

        sizes.append(os.path.getsize(f"{self.folder}/{self.type}_result.zip"))
        sizes = list(map(lambda size: round(size / 1024, 1), sizes))

        context = {'files': zip(names, files, sizes)}

        return context
