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
from generator_app.forms.IntegrationForm import IntegrationForm
from generator_app.forms.InterpolationForm import InterpolationForm
from generator_app.forms.SplinesForm import SplinesForm
from generator_app.forms.CustomVariantsForm import CustomVariantsForm
from generator_classes.TaskGenerator import TaskGenerator
from generator_classes.DocumentGenerator import DocumentGenerator


@csrf_exempt
def interpolation(request):
    form = InterpolationForm()
    return render(request, 'generator_app/interpolation.html',
                  context={'form': form})


@csrf_exempt
def integration(request):
    form = IntegrationForm()
    return render(request, 'generator_app/integration.html',
                  context={'form': form})


@csrf_exempt
def splines(request):
    form = SplinesForm()
    return render(request, 'generator_app/splines.html',
                  context={'form': form})


@csrf_exempt
def custom_variants(request):
    form = CustomVariantsForm()
    return render(request, 'generator_app/custom_variants.html',
                  context={'form': form})


def index(request):
    return render(request, 'generator_app/index.html')


def generate_interpolation(request):
    if request.method == 'POST':
        form = InterpolationForm(request.POST)
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

            tasks = information.get('tasks')
            alternate = information.get('alternate')
            structure = []
            if alternate == 'alternate':
                interpolation_tasks = []
                for task in tasks:
                    interpolation_tasks.append(task)
                structure.append(interpolation_tasks)
            elif alternate == 'not_alternate':
                for task in tasks:
                    structure.append([task])

            task_generator = TaskGenerator(structure, number_of_variants, seed)

            interpolation_parameters = {
                'degree': information.get('the_biggest_polynomial_degree')
            }

            task_generator.set_task_parameters('Interpolation', interpolation_parameters)

            # Task generation
            variants_list = task_generator.generate_tasks()

            # Document generation parameters
            filename = information.get('filename')

            generation_format = information.get('generation_format')
            generate_pdf = 'pdf' in generation_format
            generate_latex = 'tex' in generation_format

            document_generator = DocumentGenerator(task_generator.seed, filename, timestamp,
                                                   'interpolation', generate_pdf, generate_latex,
                                                   surnames)

            # Document generation
            context = document_generator.generate_document(variants_list, task_generator.seed)

            return render(request, "generator_app/result_page.html",
                          context=context)
        return render(request, "generator_app/interpolation.html",
                      context={'form': form})
    return HttpResponseNotFound('<h1>Page not found</h1>')


def generate_integration(request):
    if request.method == 'POST':
        form = IntegrationForm(request.POST)
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

            structure_string = information.get('structure')
            possible_structures = {
                'both': [['Trapezoid'], ['Simpson']],
                'Trapezoid': [['Trapezoid']],
                'Simpson': [['Simpson']],
                'alternating': [['Trapezoid', 'Simpson']]
            }
            structure = possible_structures[structure_string]
            if structure is None:
                raise ValueError('Invalid structure provided')

            task_generator = TaskGenerator(structure, number_of_variants, seed)

            trapezoid_parameters = {
                'n': information.get('number_of_trapezoidD_points')
            }

            simpson_parameters = {
                'n': information.get('number_of_Simpson_points')
            }

            task_generator.set_task_parameters('Trapezoid', trapezoid_parameters)
            task_generator.set_task_parameters('Simpson', simpson_parameters)

            # Task generation
            variants_list = task_generator.generate_tasks()

            # Document generation parameters
            filename = information.get('filename')

            generation_format = information.get('generation_format')
            generate_pdf = 'pdf' in generation_format
            generate_latex = 'tex' in generation_format

            document_generator = DocumentGenerator(task_generator.seed, filename, timestamp,
                                                   'integration', generate_pdf, generate_latex,
                                                   surnames)

            # Document generation
            context = document_generator.generate_document(variants_list, task_generator.seed)

            return render(request, "generator_app/result_page.html",
                          context=context)
        return render(request, "generator_app/integration.html",
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

            task_generator = TaskGenerator([['Spline']], number_of_variants, seed)

            spline_parameters = {
                'x1': information.get('Splines_x1'),
                'x2': information.get('Splines_x2'),
                'y1': information.get('Splines_y1'),
                'y2': information.get('Splines_y2'),
                'step': information.get('Splines_step')
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
                                                   'splines', generate_pdf, generate_latex,
                                                   surnames)

            # Document generation
            context = document_generator.generate_document(variants_list, task_generator.seed)

            return render(request, "generator_app/result_page.html",
                          context=context)
        return render(request, "generator_app/splines.html",
                      context={'form': form})
    return HttpResponseNotFound('<h1>Page not found</h1>')


def generate_custom(request):
    if request.method == 'POST':
        form = CustomVariantsForm(request.POST)
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

            tasks = information.get('tasks')
            structure = []

            alternate = information.get('alternate')
            if 'alternate_interpolation' in alternate:
                interpolation_tasks = []
                for task in tasks:
                    if 'Interpolation' in task:
                        interpolation_tasks.append(task)
                if len(interpolation_tasks) != 0:
                    tasks = [task for task in tasks if 'Interpolation' not in task]
                    structure.append(interpolation_tasks)

            if 'alternate_integration' in alternate:
                integration_tasks = []
                for task in tasks:
                    if ('Simpson' in task) or ('Trapezoid' in task):
                        integration_tasks.append(task)
                if len(integration_tasks) != 0:
                    tasks = [task for task in tasks if 'Trapezoid' not in task and 'Simpson' not in task]
                    structure.append(integration_tasks)

            for task in tasks:
                structure.append([task])

            task_generator = TaskGenerator(structure, number_of_variants, seed)

            if 'Interpolation' in structure:
                interpolation_parameters = {
                    'degree': information.get('the_biggest_polynomial_degree')
                }
                task_generator.set_task_parameters('Interpolation', interpolation_parameters)

            if 'Spline' in structure:
                spline_parameters = {
                    'x1': information.get('Splines_x1'),
                    'x2': information.get('Splines_x2'),
                    'y1': information.get('Splines_y1'),
                    'y2': information.get('Splines_y2'),
                    'step': information.get('Splines_step')
                }
                task_generator.set_task_parameters('Spline', spline_parameters)

            if 'Trapezoid' in structure:
                trapezoid_parameters = {
                    'n': information.get('number_of_trapezoid_points')
                }
                task_generator.set_task_parameters('Trapezoid', trapezoid_parameters)

            if 'Simpson' in structure:
                simpson_parameters = {
                    'n': information.get('number_of_Simpson_points')
                }
                task_generator.set_task_parameters('Simpson', simpson_parameters)

            # Task generation
            variants_list = task_generator.generate_tasks()

            # Document generation parameters
            filename = information.get('filename')

            generation_format = information.get('generation_format')
            generate_pdf = 'pdf' in generation_format
            generate_latex = 'tex' in generation_format

            document_generator = DocumentGenerator(task_generator.seed, filename, timestamp,
                                                   'custom', generate_pdf, generate_latex)

            # Document generation
            context = document_generator.generate_document(variants_list, task_generator.seed)

            return render(request, "generator_app/result_page.html",
                          context=context)
        return render(request, "generator_app/custom_variants.html",
                      context={'form': form})
    return HttpResponseNotFound('<h1>Page not found</h1>')
