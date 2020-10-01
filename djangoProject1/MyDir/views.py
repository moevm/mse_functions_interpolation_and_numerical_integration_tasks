from django.shortcuts import render


def MyDir(request):

    return render(request, 'MyDir/index.html',locals())