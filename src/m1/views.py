from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'title': 'US Rifle M1.com'
    }
    return render(request, 'm1/index.html', context)
