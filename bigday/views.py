import os
from django.shortcuts import render
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def get_file_names(url):
    return os.listdir(url)

def gallery(request):
    picture_names = list(filter(lambda x: x != 'cache', get_file_names("media/photologue/photos")))
    return render(request, 'gallery.html', {'photos': picture_names})