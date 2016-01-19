from django.conf.urls import url

from . import views
from guests.views import GuestListView, test_email, save_the_date_preview, save_the_date_random

urlpatterns = [
    url(r'^$', save_the_date_random, name='save-the-date-random'),
    url(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    url(r'^save-the-date/(?P<template_id>[\w-]+)/$', save_the_date_preview, name='save-the-date'),
    url(r'^email-test/(?P<template_id>[\w-]+)/$', test_email, name='test-email'),
]
