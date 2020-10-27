from django.http import HttpResponse
from django.shortcuts import render
# from interpolation.Tasks import Tasks
from Generator.interpolation.Tasks import Tasks


def index(request):
    return render(request, "interpolation_integration_generator/index.html", {})

def generate_interpolations(request):
    # print(2)
    # print(request)
    # number_in_string = request.GET["number"]
    # degree = request.GET[""]
    options_in_line = 3
    options_summary = 10
    degree = 4

    document = Tasks(options_summary, options_in_line, degree)
    document.generate()

    response = HttpResponse(mimetype='application/pdf')
    response["Content-Disposition"] = 'attachment; filename=tasks.pdf'
    return response
