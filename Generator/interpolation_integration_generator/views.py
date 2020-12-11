import asyncio
import os
import zipfile
from datetime import datetime
from os.path import basename

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from integration.main import run
from interpolation.Tasks import Tasks
from interpolation_integration_generator.forms.IntegrationForm import IntegrationForm
from interpolation_integration_generator.forms.InterpolationForm import InterpolationForm


@csrf_exempt
def interpolation(request):
    form = InterpolationForm()
    return render(request, 'interpolation_integration_generator/interpolation.html', context={'form': form})


@csrf_exempt
def integration(request):
    form = IntegrationForm()
    return render(request, 'interpolation_integration_generator/integration.html', context={'form': form})


def index(request):
    return render(request, 'interpolation_integration_generator/index.html')


def generate_interpolation(request):
    if request.method == 'POST':
        form = InterpolationForm(request.POST)
        if form.is_valid():
            information = form.cleaned_data

            names = []
            files = []
            sizes = []

            timestamp = str(datetime.now()).replace(":", "-").replace(" ", "_")
            folder = f'interpolation_integration_generator/static/interpolation_integration_generator/{timestamp}'
            static_folder = f"/static/interpolation_integration_generator/{timestamp}"
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

            document = Tasks(number_of_variants, number_of_variants_in_string, the_biggest_polynomial_degree, seed)
            loop = asyncio.new_event_loop()
            loop.run_until_complete(document.generate(filename, is_pdf, is_tex, timestamp, surnames))
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

            return render(request, "interpolation_integration_generator/result_page.html", context=context)
        # return render(request, 'interpolation_integration_generator/index.html', {'form': form})


def generate_integration(request):
    if request.method == 'POST':
        form = IntegrationForm(request.POST)
        if form.is_valid():
            information = form.cleaned_data
            names = []
            files = []
            sizes = []

            timestamp = str(datetime.now()).replace(":", "-").replace(" ", "_")
            folder = f'interpolation_integration_generator/static/interpolation_integration_generator/{timestamp}'
            static_folder = f"/static/interpolation_integration_generator/{timestamp}"
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
                run(options_count, SimpsonPointsCnt, TrapezoidPointsCnt, filename, is_pdf, is_tex, timestamp, seed,
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

            return render(request, "interpolation_integration_generator/result_page.html", context=context)
