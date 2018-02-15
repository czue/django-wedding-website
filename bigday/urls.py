from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
    #     home_files, name='home-files'),
]

urlpatterns += i18n_patterns(
    url(r'^', include('wedding.urls')),
    url(r'^', include('guests.urls')),
    url('^accounts/', include('django.contrib.auth.urls'))
)
