from django.urls import re_path, include
from django.contrib import admin


urlpatterns = [
    re_path(r'^', include('wedding.urls')),
    re_path(r'^', include('guests.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path('^accounts/', include('django.contrib.auth.urls'))
]
