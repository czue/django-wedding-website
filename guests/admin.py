from django.contrib import admin
from .models import Guest, Party


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'category', 'save_the_date_sent', 'is_invited')
    list_filter = ('type', 'category', 'is_invited')


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'email', 'is_attending')
    list_filter = ('is_attending',)


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
