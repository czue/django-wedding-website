from __future__ import unicode_literals
import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from django import forms

FAMILY_SIDE = [
    ('kim', 'Kim'),
    ('jacob', 'Jacob'),
]

def _random_uuid():
    return uuid.uuid4().hex


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    family = models.CharField(max_length=10, choices=FAMILY_SIDE, default="")
    address = models.CharField(max_length=1024, default="")
    save_the_date_sent = models.DateTimeField(null=True, blank=True, default=None)
    save_the_date_opened = models.DateTimeField(null=True, blank=True, default=None)
    invitation_id = models.CharField(max_length=32, db_index=True, default=_random_uuid, unique=True)
    invitation_sent = models.DateTimeField(null=True, blank=True, default=None)
    invitation_opened = models.DateTimeField(null=True, blank=True, default=None)
    is_invited = models.BooleanField(default=False)
    is_attending = models.NullBooleanField(default=None)
    comments = models.TextField(null=True, blank=True)
    name_update_comments = models.TextField(null=True, blank=True)
    rsvp_code = models.CharField(max_length=32, default="")

    def __str__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('family', '-is_invited', 'name')

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('is_child', 'pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return list(filter(None, self.guest_set.values_list('email', flat=True)))


MEALS = [
    ('chicken', 'chicken'),
    ('beef', 'beef'),
    ('salmon', 'salmon'),
    ('vegetarian', 'vegetarian'),
    ('kidsmeal', 'kids meal'),
]


class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    is_attending = models.NullBooleanField(default=None)
    tea_ceremony = models.BooleanField(default=False)
    meal = models.CharField(max_length=20, choices=MEALS, null=True, blank=True)
    is_child = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    def __str__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)

class RsvpForm(forms.Form): 
    rsvp_code = forms.CharField(max_length = 32)#, help_text="<br><em> This will be your first name and last name with no caps or spaces (e.g. renerjacob) </em>")
    
    def __str__(self):
        return self.name

class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': False}),
        }
#Continue from here for next time
class testUpdateInfoForm(forms.Form): 
    first_name = forms.TextInput(attrs={'required': True}),
    last_name = forms.TextInput(attrs={'required': True}),
    email = forms.EmailInput(attrs={'required': True}),