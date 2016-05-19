from django.contrib import admin
from .models import Guest, Party


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('first_name', 'last_name', 'email', 'is_attending', 'meal', 'is_child')
    readonly_fields = ('first_name', 'last_name', 'email')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'category', 'save_the_date_sent', 'invitation_sent', 'rehearsal_dinner', 'invitation_opened',
                    'is_invited', 'is_attending')
    list_filter = ('type', 'category', 'is_invited', 'is_attending', 'rehearsal_dinner', 'invitation_opened')
    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'email', 'is_attending', 'is_child', 'meal')
    list_filter = ('is_attending', 'is_child', 'meal', 'party__is_invited', 'party__category', 'party__rehearsal_dinner')


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
