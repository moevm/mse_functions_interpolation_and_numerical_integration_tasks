import asyncio
import os
from numpy import random
import zipfile
from datetime import datetime
from os.path import basename

from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Tasks.IntegrationTask import run
from Tasks.InterpolationDocument import InterpolationDocument
from generator.forms.IntegrationForm import IntegrationForm
from generator.forms.InterpolationForm import InterpolationForm
from generator.forms.SplinesForm import SplinesForm
from generator.forms.CustomVariantsForm import CustomVariantsForm
from generator_classes.TaskGenerator import TaskGenerator
from generator_classes.DocumentGenerator import DocumentGenerator


@csrf_exempt
def interpolation(request):
    form = InterpolationForm()
    return render(request, 'generator/interpolation.html',
                  context={'form': form})


@csrf_exempt
def integration(request):
    form = IntegrationForm()
    return render(request, 'generator/integration.html',
                  context={'form': form})


@csrf_exempt
def splines(request):
    form = SplinesForm()
    return render(request, 'generator/splines.html',
                  context={'form': form})


@csrf_exempt
def custom_variants(request):
    form = CustomVariantsForm()
    return render(request, 'generator/custom_variants.html',
                  context={'form': form})


def index(request):
    return render(request, 'generator/index.html')


def generate_interpolation(request):
    if request.method == 'POST':
        form = InterpolationForm(request.POST)
        if form.is_valid():
            information = form.cleaned_data

            names = []
            files = []
            sizes = []

            timestamp = str(datetime.now()).replace(":", "-").replace(" ", "_")
            folder = os.path.join(
                settings.BASE_DIR,
                'generator',
                'static',
                'generator',
                'variants',
                timestamp
            )
            #            folder = f'generator/static/generator/{timestamp}'
            static_folder = f"/static/generator/variants/{timestamp}"
            os.mkdir(f"{folder}")

            filename = information.get('filename')
            number_of_variants_in_string = information.get("number_of_variants_in_string")
            the_biggest_polynomial_degree = information.get("the_biggest_polynomial_degree")
            generation_format = information.get('generation_format')
            seed = information.get("seed")
            variants_type = information.get("variants_type")
            is_pdf = 'pdf' in generation_format
            is_tex = 'tex' in generation_format

            if variants_type == "digits":
                surnames = None
                number_of_variants = information.get("number_of_variants")
            elif variants_type == 'surnames':
                surnames = request.FILES['file_with_surnames'].read().decode("utf-8").splitlines()
                number_of_variants = len(surnames)

            document = InterpolationDocument(number_of_variants, number_of_variants_in_string,
                                             the_biggest_polynomial_degree, seed)
            loop = asyncio.new_event_loop()
            loop.run_until_complete(
                document.generate(filename, is_pdf, is_tex, timestamp, surnames))
            loop.close()

            filenames = []
            if is_pdf:
                filenames.append(f"{folder}/interpolation_{filename}.pdf")
                filenames.append(f'{folder}/interpolation_answers_for_{filename}.pdf')

                names.append(f"interpolation_{filename}.pdf")
                files.append(f"{static_folder}/interpolation_{filename}.pdf")
                sizes.append(os.path.getsize(f"{folder}/interpolation_{filename}.pdf"))

                names.append(f"interpolation_answers_for_{filename}.pdf")
                files.append(f"{static_folder}/interpolation_answers_for_{filename}.pdf")
                sizes.append(os.path.getsize(f"{folder}/interpolation_answers_for_{filename}.pdf"))

            if is_tex:
                filenames.append(f"{folder}/interpolation_{filename}.tex")
                filenames.append(f'{folder}/interpolation_answers_for_{filename}.tex')

                names.append(f"interpolation_{filename}.tex")
                files.append(f"{static_folder}/interpolation_{filename}.tex")
                sizes.append(os.path.getsize(f"{folder}/interpolation_{filename}.tex"))

                names.append(f"interpolation_answers_for_{filename}.tex")
                files.append(f"{static_folder}/interpolation_answers_for_{filename}.tex")
                sizes.append(os.path.getsize(f"{folder}/interpolation_answers_for_{filename}.tex"))

            with zipfile.ZipFile(f'{folder}/interpolation_result.zip', 'w') as zipObj:
                for file in filenames:
                    zipObj.write(file, basename(file))

            names.append("interpolation_result.zip")
            files.append(f"{static_folder}/interpolation_result.zip")

            sizes.append(os.path.getsize(f"{folder}/interpolation_result.zip"))
            sizes = list(map(lambda size: round(size / 1024, 1), sizes))

            context = {'files': zip(names, files, sizes)}

            return render(request, "generator/result_page.html",
                          context=context)
        return render(request, "generator/interpolation.html",
                      context={'form': form})
    return HttpResponseNotFound('<h1>Page not found</h1>')


def generate_integration(request):
    if request.method == 'POST':
        form = IntegrationForm(request.POST)
        if form.is_valid():
            information = form.cleaned_data
            names = []
            files = []
            sizes = []

            timestamp = str(datetime.now()).replace(":", "-").replace(" ", "_")
            folder = os.path.join(
                settings.BASE_DIR,
                'generator',
                'static',
                'generator',
                'variants',
                timestamp
            )
            #           folder = f'generator/static/generator/{timestamp}'
            static_folder = f"/static/generator/variants/{timestamp}"
            os.mkdir(f"{folder}")

            filename = information.get('filename')
            TrapezoidPointsCnt = information.get("number_of_trapezoid_points")
            SimpsonPointsCnt = information.get("number_of_Simpson_points")
            generation_format = information.get('generation_format')

            is_pdf = 'pdf' in generation_format
            is_tex = 'tex' in generation_format
            seed = information.get("seed")
            variants_type = information.get("variants_type")

            if variants_type == "digits":
                surnames = None
                options_count = information.get("number_of_variants")
            elif variants_type == 'surnames':
                surnames = request.FILES['file_with_surnames'].read().decode("utf-8").splitlines()
                options_count = len(surnames)

            loop = asyncio.new_event_loop()
            loop.run_until_complete(
                run(options_count, SimpsonPointsCnt, TrapezoidPointsCnt, filename, is_pdf, is_tex,
                    timestamp, seed,
                    surnames))
            loop.close()

            filenames = []

            if is_pdf:
                filenames.append(f"{folder}/integration_{filename}.pdf")
                filenames.append(f'{folder}/integration_answers_for_{filename}.pdf')

                names.append(f"integration_{filename}.pdf")
                files.append(f"{static_folder}/integration_{filename}.pdf")
                sizes.append(os.path.getsize(f"{folder}/integration_{filename}.pdf"))

                names.append(f"integration_answers_for_{filename}.pdf")
                files.append(f"{static_folder}/integration_answers_for_{filename}.pdf")
                sizes.append(os.path.getsize(f"{folder}/integration_answers_for_{filename}.pdf"))

            if is_tex:
                filenames.append(f"{folder}/integration_{filename}.tex")
                filenames.append(f'{folder}/integration_answers_for_{filename}.tex')

                names.append(f"integration_{filename}.tex")
                files.append(f"{static_folder}/integration_{filename}.tex")
                sizes.append(os.path.getsize(f"{folder}/integration_{filename}.tex"))

                names.append(f"integration_answers_for_{filename}.tex")
                files.append(f"{static_folder}/integration_answers_for_{filename}.tex")
                sizes.append(os.path.getsize(f"{folder}/integration_answers_for_{filename}.tex"))

            with zipfile.ZipFile(f'{folder}/integration_result.zip', 'w') as zipObj:
                for file in filenames:
                    zipObj.write(file, basename(file))

            names.append("integration_result.zip")
            files.append(f"{static_folder}/integration_result.zip")

            sizes.append(os.path.getsize(f"{folder}/integration_result.zip"))
            sizes = list(map(lambda size: round(size / 1024, 1), sizes))

            context = {'files': zip(names, files, sizes)}

            return render(request, "generator/result_page.html",
                          context=context)
        return render(request, "generator/integration.html",
                      context={'form': form})
    return HttpResponseNotFound('<h1>Page not found</h1>')


def generate_splines(request):
    if request.method == 'POST':
        form = SplinesForm(request.POST)
        if form.is_valid():
            timestamp = str(datetime.now()).replace(":", "-").replace(" ", "_")

            information = form.cleaned_data

            # Task generation parameters
            variants_type = information.get("variants_type")
            if variants_type == "digits":
                surnames = None
                number_of_variants = information.get("number_of_variants")
            elif variants_type == 'surnames':
                surnames = request.FILES['file_with_surnames'].read().decode("utf-8").splitlines()
                number_of_variants = len(surnames)

            seed = information.get("seed")
            if seed is None:
                seed = random.randint(0, 1000000)

            task_generator = TaskGenerator(['Spline'], number_of_variants, seed)

            spline_parameters = {
                'x1': information.get('x1'),
                'x2': information.get('x2'),
                'y1': information.get('y1'),
                'y2': information.get('y2'),
                'step': information.get('step')
            }

            task_generator.set_task_parameters('Spline', spline_parameters)

            # Task generation
            variants_list = task_generator.generate_tasks()

            # Document generation parameters
            filename = information.get('filename')

            generation_format = information.get('generation_format')
            generate_pdf = 'pdf' in generation_format
            generate_latex = 'tex' in generation_format

            document_generator = DocumentGenerator(task_generator.seed, filename, timestamp,
                                                   generate_pdf, generate_latex)

            # Document generation
            context = document_generator.generate_document(variants_list, task_generator.seed)

            return render(request, "generator/result_page.html",
                          context=context)
        return render(request, "generator/splines.html",
                      context={'form': form})
    return HttpResponseNotFound('<h1>Page not found</h1>')
