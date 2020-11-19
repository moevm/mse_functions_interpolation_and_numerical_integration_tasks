import os
import zipfile
from datetime import datetime
from os.path import basename

from django.http import HttpResponse
from django.shortcuts import render
from integration.main import run
from interpolation.Tasks import Tasks


def index(request):
    return render(request, "interpolation_integration_generator/index.html", {})


async def generate_interpolations(request):
    names = []
    files = []
    sizes = []

    timestamp = str(datetime.now()).replace(":", "-").replace(" ", "_")
    folder = f'interpolation_integration_generator/static/interpolation_integration_generator/{timestamp}'
    static_folder = f"/static/interpolation_integration_generator/{timestamp}"
    os.mkdir(f"{folder}")

    options_in_line = int(request.GET.get("number"))
    degree = int(request.GET.get("degree"))
    options_summary = int(request.GET.get("options_summary"))

    is_pdf = True if request.GET.get("saveOnPDF") == "Yes" else False
    is_latex = True if request.GET.get("saveOnLaTex") == "Yes" else False
    filename = request.GET.get("filename")
    seed = None
    try:
        seed = int(request.GET.get("seed"))
    except ValueError:
        pass

    document = Tasks(options_summary, options_in_line, degree, seed)
    document.generate(filename, is_pdf, is_latex, timestamp)

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


async def generate_integration(request):
    names = []
    files = []
    sizes = []

    timestamp = str(datetime.now()).replace(":", "-").replace(" ", "_")
    folder = f'interpolation_integration_generator/static/interpolation_integration_generator/{timestamp}'
    static_folder = f"/static/interpolation_integration_generator/{timestamp}"
    os.mkdir(f"{folder}")

    variantsCnt = int(request.GET.get("variantsCnt"))
    TrapezoidPointsCnt = int(request.GET.get("TrapezoidPointsCnt"))
    SimpsonPointsCnt = int(request.GET.get("SimpsonPointsCnt"))

    is_pdf = True if request.GET.get("saveOnPDF") == "Yes" else False
    is_latex = True if request.GET.get("saveOnLaTex") == "Yes" else False
    filename = request.GET.get("fileName")

    run(variantsCnt, SimpsonPointsCnt, TrapezoidPointsCnt, filename, is_pdf, is_latex, timestamp)

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
