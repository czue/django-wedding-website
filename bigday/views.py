import os

from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def get_file_names_by_prefix(url, prefix):
    list_filenames = os.listdir(url)
    finalList = []
    for filename in list_filenames:
        if filename.startswith(prefix):
            finalList.append(filename)
    return finalList

def g_home(request):
    return render(request, 'gallery-home.html')

def g_pro(request):
    return render(request, 'gallery.html', {'photos': get_file_names_by_prefix("media/photologue/photos", 'pro_')})

def g_friends(request):
    return render(request, 'gallery.html', {'photos': get_file_names_by_prefix("media/photologue/photos", 'friends_')})

def g_others(request):
    return render(request, 'gallery.html', {'photos': get_file_names_by_prefix("media/photologue/photos", 'others_')})