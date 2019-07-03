import os
from django.shortcuts import render
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def get_file_names(url):
    return os.listdir(url)


def g_home(request):
    return render(request, 'gallery-home.html')

def g_pro(request):
    picture_names = list(filter(lambda x: x != 'cache', get_file_names("media/photologue/photos/pro")))
    return render(request, 'gallery.html', {'photos': picture_names})

def g_perso(request):
    picture_names = list(filter(lambda x: x != 'cache', get_file_names("media/photologue/photos/perso")))
    return render(request, 'gallery.html', {'photos': picture_names})

def g_other(request):
    picture_names = list(filter(lambda x: x != 'cache', get_file_names("media/photologue/photos/other")))
    return render(request, 'gallery.html', {'photos': picture_names})