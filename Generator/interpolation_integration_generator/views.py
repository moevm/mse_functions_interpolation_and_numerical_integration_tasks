import zipfile
from os.path import basename
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.shortcuts import render
from interpolation.Tasks import Tasks
from integration.main import run


def index(request):
    return render(request, "interpolation_integration_generator/index.html", {})


@csrf_exempt
def generate_interpolations(request):
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
        options_summary = request.POST.get("options_summary")
    else:
        surnames = request.FILES['surnameFile'].read().decode("utf-8").splitlines()
        options_summary = len(surnames)

    document = Tasks(options_summary, options_in_line, degree, seed)
    document.generate(filename, is_pdf, is_latex, surnames)

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


@csrf_exempt
def generate_integration(request):
    TrapezoidPointsCnt = int(request.POST.get("TrapezoidPointsCnt"))
    SimpsonPointsCnt = int(request.POST.get("SimpsonPointsCnt"))

    is_pdf = True if request.POST.get("saveOnPDF") == "Yes" else False
    is_latex = True if request.POST.get("saveOnLaTex") == "Yes" else False
    filename = request.POST.get("fileName")

    variantsType = request.POST.get("Numbering")

    if variantsType == "Digits":
        run(int(request.POST.get("variantsCnt")), SimpsonPointsCnt, TrapezoidPointsCnt, filename, is_pdf, is_latex)
    else:
        surnames = request.FILES['surnameFile'].read().decode("utf-8").splitlines()
        run(len(surnames), SimpsonPointsCnt, TrapezoidPointsCnt, filename, is_pdf, is_latex, surnames)

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