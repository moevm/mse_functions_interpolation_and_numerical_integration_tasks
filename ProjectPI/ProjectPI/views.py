from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse


def show(request):
    return render(request, 'index.html')


def download(request):

    myDict = request.GET

    if myDict.get('saveOnPDF', '') == '' and myDict.get('saveOnLaTex', '') == '':
        return HttpResponse("Все очень плохо")
    return render(request, 'page.html')
