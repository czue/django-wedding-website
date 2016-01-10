from django.contrib import admin
from .models import Guest

class GuestAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'save_the_date_sent', 'save_the_date_opened', 'invited', 'attending')
    list_filter = ('save_the_date_sent', 'save_the_date_opened', 'invited', 'attending')


admin.site.register(Guest, GuestAdmin)


