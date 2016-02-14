from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<tracking_category>[\w-]+)/(?P<tracking_id>[\w-]+).jpg$', views.track_open, name='track-open'),
]
