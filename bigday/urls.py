from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('wedding.urls')),
    url(r'^', include('guests.urls')),
    url(r'^admin/', admin.site.urls),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('i18n/', include('django.conf.urls.i18n'))
]
