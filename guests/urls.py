from django.conf.urls import url

from . import views
from guests.views import GuestListView, test_email, save_the_date_preview

urlpatterns = [
    url(r'^$', GuestListView.as_view(), name='guest-list'),
    url(r'^save-the-date/(?P<template_id>[\w-]+)/$', save_the_date_preview, name='save-the-date'),
    url(r'^email-test/(?P<template_id>[\w-]+)/$', test_email, name='test-email'),
]
