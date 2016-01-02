from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return render(request, 'base.html')
    return render(request, 'home.html')


def story(request):
    # return render(request, 'base.html')
    return render(request, 'story.html')
