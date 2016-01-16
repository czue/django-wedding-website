from django.conf.urls import url

from . import views
from guests.views import GuestListView, test_email, RoEmailPreviewView, CoryEmailPreviewView

urlpatterns = [
    url(r'^$', GuestListView.as_view(), name='guest-list'),
    url(r'^save-the-date/', RoEmailPreviewView.as_view(), name='save-the-date'),
    url(r'^save-the-date-cory/', CoryEmailPreviewView.as_view(), name='save-the-date-cory'),
    url(r'^email-test/', test_email, name='test-email'),
]
