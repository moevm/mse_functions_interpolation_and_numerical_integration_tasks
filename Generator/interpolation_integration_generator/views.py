import zipfile
from os.path import basename

from django.http import HttpResponse
from django.shortcuts import render
from interpolation.Tasks import Tasks
import os


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
        int(request.GET.get("seed"))
    except Exception:
        pass
    else:
        seed = int(request.GET.get("seed"))

    document = Tasks(options_summary, options_in_line, degree)
    document.generate(filename, is_pdf, is_latex, seed)

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

    # удаляем сгенеринные pdf и tex после их записи в возвращаемый архив
    if is_pdf:
        os.remove(f"{folder}/{filename}.pdf")
        os.remove(f'{folder}/answers_for_{filename}.pdf')
    if is_latex:
        os.remove(f"{folder}/{filename}.tex")
        os.remove(f'{folder}/answers_for_{filename}.tex')

    return response
