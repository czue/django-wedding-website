from django.contrib import admin
from .models import Guest, Party


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('first_name', 'last_name', 'email', 'party', 'is_attending', 'meal', 'is_child')
    readonly_fields = ('first_name', 'last_name', 'email')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'rsvp_code', 'invitation_opened', 'is_attending', 'name_update_comments', 'comments')
    list_filter = ('is_attending', 'invitation_opened')
    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_attending', 'party', 'is_child', 'meal')
    list_filter = ('is_attending', 'is_child', 'meal')


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
