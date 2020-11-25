import asyncio
import os
import zipfile
from datetime import datetime
from os.path import basename

from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.shortcuts import render
from integration.main import run
from interpolation.Tasks import Tasks


def index(request):
    return render(request, "interpolation_integration_generator/index.html", {})

@csrf_exempt
def generate_interpolations(request):
    names = []
    files = []
    sizes = []

    timestamp = str(datetime.now()).replace(":", "-").replace(" ", "_")
    folder = f'interpolation_integration_generator/static/interpolation_integration_generator/{timestamp}'
    static_folder = f"/static/interpolation_integration_generator/{timestamp}"
    os.mkdir(f"{folder}")

    options_in_line = int(request.POST.get("number"))
    degree = int(request.POST.get("degree"))

    is_pdf = True if request.POST.get("saveOnPDF") == "Yes" else False
    is_latex = True if request.POST.get("saveOnLaTex") == "Yes" else False
    filename = request.POST.get("filename")
    seed = None
    try:
        seed = int(request.POST.get("seed"))
    except ValueError:
        pass

    variantsType = request.POST.get("Numbering")

    surnames = None
    options_summary = 0
    if variantsType == "Digits":
        options_summary = int(request.POST.get("options_summary"))
    else:
        surnames = request.FILES['file'].read().decode("utf-8").splitlines()
        options_summary = len(surnames)

    document = Tasks(options_summary, options_in_line, degree, seed)
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(document.generate(filename, is_pdf, is_latex, timestamp, surnames))
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

    if is_latex:
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

    sizes = list(map(lambda size: round(size/1024, 1), sizes))
    sizes.append(os.path.getsize(f"{folder}/interpolation_result.zip"))

    context = {'files': zip(names, files, sizes)}

    return render(request, "interpolation_integration_generator/result_page.html", context=context)

@csrf_exempt
def generate_integration(request):
    names = []
    files = []
    sizes = []

    timestamp = str(datetime.now()).replace(":", "-").replace(" ", "_")
    folder = f'interpolation_integration_generator/static/interpolation_integration_generator/{timestamp}'
    static_folder = f"/static/interpolation_integration_generator/{timestamp}"
    os.mkdir(f"{folder}")

    TrapezoidPointsCnt = int(request.POST.get("TrapezoidPointsCnt"))
    SimpsonPointsCnt = int(request.POST.get("SimpsonPointsCnt"))

    is_pdf = True if request.POST.get("saveOnPDF") == "Yes" else False
    is_latex = True if request.POST.get("saveOnLaTex") == "Yes" else False
    filename = request.POST.get("fileName")

    variantsType = request.POST.get("Numbering")

    options_count = None
    surnames = None

    if variantsType == "Digits":
        options_count = int(request.POST.get("variantsCnt"))
    else:
        surnames = request.FILES['file'].read().decode("utf-8").splitlines()
        options_count = len(surnames)

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(run(options_count, SimpsonPointsCnt, TrapezoidPointsCnt, filename, is_pdf, is_latex, timestamp,
                                         request.POST.get("seed"), surnames))
    loop.close()

    # folder = 'interpolation_integration_generator/static/interpolation_integration_generator'
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

    if is_latex:
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

    sizes = list(map(lambda size: round(size/1024, 1), sizes))
    sizes.append(os.path.getsize(f"{folder}/integration_result.zip"))

    context = {'files': zip(names, files, sizes)}

    return render(request, "interpolation_integration_generator/result_page.html", context=context)
