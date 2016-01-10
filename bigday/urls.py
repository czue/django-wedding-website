from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'', include('wedding.urls')),
    url(r'^guests/', include('guests.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^admin/', admin.site.urls),
    url('^accounts/', include('django.contrib.auth.urls'))

]
