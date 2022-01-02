from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', include('wedding.urls')),
    path('', include('guests.urls')),
    path('admin/', admin.site.urls),
    #url('^accounts/', include('django.contrib.auth.urls'))
]
