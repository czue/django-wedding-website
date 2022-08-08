from django.urls import re_path

from guests.views import GuestListView, test_email, save_the_date_preview, save_the_date_random, export_guests, \
    invitation, invitation_email_preview, invitation_email_test, rsvp_confirm, dashboard

urlpatterns = [
    re_path(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    re_path(r'^dashboard/$', dashboard, name='dashboard'),
    re_path(r'^guests/export$', export_guests, name='export-guest-list'),
    re_path(r'^invite/(?P<invite_id>[\w-]+)/$', invitation, name='invitation'),
    re_path(r'^invite-email/(?P<invite_id>[\w-]+)/$', invitation_email_preview, name='invitation-email'),
    re_path(r'^invite-email-test/(?P<invite_id>[\w-]+)/$', invitation_email_test, name='invitation-email-test'),
    re_path(r'^save-the-date/$', save_the_date_random, name='save-the-date-random'),
    re_path(r'^save-the-date/(?P<template_id>[\w-]+)/$', save_the_date_preview, name='save-the-date'),
    re_path(r'^email-test/(?P<template_id>[\w-]+)/$', test_email, name='test-email'),
    re_path(r'^rsvp/confirm/(?P<invite_id>[\w-]+)/$', rsvp_confirm, name='rsvp-confirm'),
]
