from django.contrib import admin
from .models import Guest, Party


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'category')
    list_filter = ('type', 'category')


class GuestAdmin(admin.ModelAdmin):
    list_display = ('party', 'first_name', 'last_name', 'email', 'is_attending')
    list_filter = ('is_attending',)


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
