from django.conf.urls import url

from guests.views import GuestListView, test_email, save_the_date_preview, save_the_date_random, export_guests, \
    invitation, invitation_email_preview, invitation_email_test, rsvp_confirm, dashboard

urlpatterns = [
    url(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^guests/export$', export_guests, name='export-guest-list'),
    url(r'^invite/(?P<invite_id>[\w-]+)/$', invitation, name='invitation'),
    url(r'^invite-email/(?P<invite_id>[\w-]+)/$', invitation_email_preview, name='invitation-email'),
    url(r'^invite-email-test/(?P<invite_id>[\w-]+)/$', invitation_email_test, name='invitation-email-test'),
    url(r'^save-the-date/$', save_the_date_random, name='save-the-date-random'),
    url(r'^save-the-date/(?P<template_id>[\w-]+)/$', save_the_date_preview, name='save-the-date'),
    url(r'^email-test/(?P<template_id>[\w-]+)/$', test_email, name='test-email'),
    url(r'^rsvp/confirm/(?P<invite_id>[\w-]+)/$', rsvp_confirm, name='rsvp-confirm'),
]
