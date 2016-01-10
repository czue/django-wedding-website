from django.conf.urls import url

from . import views
from guests.views import GuestListView, EmailPreviewView

urlpatterns = [
    url(r'^$', GuestListView.as_view(), name='guest-list'),
    url(r'^save-the-date/', EmailPreviewView.as_view(), name='guest-list'),
]
