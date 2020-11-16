import zipfile
from os.path import basename

from django.http import HttpResponse
from django.shortcuts import render
from interpolation.Tasks import Tasks
from integration.main import run

def index(request):
    return render(request, "interpolation_integration_generator/index.html", {})


def generate_interpolations(request):
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
    document.generate(filename, is_pdf, is_latex)

    folder = 'interpolation_integration_generator/static/interpolation_integration_generator'
    filenames = []
    if is_pdf:
        filenames.append(f"{folder}/{filename}.pdf")
        filenames.append(f'{folder}/answers_for_{filename}.pdf')

    if is_latex:
        filenames.append(f"{folder}/{filename}.tex")
        filenames.append(f'{folder}/answers_for_{filename}.tex')

    with zipfile.ZipFile(f'{folder}/result.zip', 'w') as zipObj:
        for file in filenames:
            zipObj.write(file, basename(file))
    response = HttpResponse(open(f'{folder}/result.zip', 'rb'))
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = f'attachment; filename="{folder}/result.zip"'

    return response


def generate_integration(request):
    variantsCnt = int(request.GET.get("variantsCnt"))
    TrapezoidPointsCnt = int(request.GET.get("TrapezoidPointsCnt"))
    SimpsonPointsCnt = int(request.GET.get("SimpsonPointsCnt"))

    is_pdf = True if request.GET.get("saveOnPDF") == "Yes" else False
    is_latex = True if request.GET.get("saveOnLaTex") == "Yes" else False
    filename = request.GET.get("fileName")

    run(variantsCnt, SimpsonPointsCnt, TrapezoidPointsCnt, filename, is_pdf, is_latex)

    folder = 'interpolation_integration_generator/static/interpolation_integration_generator'
    filenames = []

    if is_pdf:
        filenames.append(f"{folder}/integration_{filename}.pdf")
        filenames.append(f'{folder}/integration_answers_for_{filename}.pdf')

    if is_latex:
        filenames.append(f"{folder}/integration_{filename}.tex")
        filenames.append(f'{folder}/integration_answers_for_{filename}.tex')

    with zipfile.ZipFile(f'{folder}/integration_result.zip', 'w') as zipObj:
        for file in filenames:
            zipObj.write(file, basename(file))
    response = HttpResponse(open(f'{folder}/integration_result.zip', 'rb'))
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = f'attachment; filename="{folder}/integration_result.zip"'

    return response