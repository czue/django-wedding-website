import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


def _random_uuid():
    return uuid.uuid4().hex


LANGS = [
    ('en', 'en'),
    ('es', 'es'),
    ('fr', 'fr'),
]


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    invitation_id = models.CharField(max_length=32, db_index=True, default=_random_uuid, unique=True)
    lang = models.CharField(max_length=2, choices=LANGS, null=True, blank=True)
    invitation_sent = models.DateTimeField(null=True, blank=True, default=None)
    invitation_opened = models.DateTimeField(null=True, blank=True, default=None)
    is_invited = models.BooleanField(default=False)
    is_attending = models.NullBooleanField(default=None)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('-is_invited', 'name')

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('is_child', 'pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return filter(None, self.guest_set.values_list('email', flat=True))


MEALS = [
    ('meat', _('meat option')),
    ('vegetarian', _('vegetarian option')),
]

class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey(Party, models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    is_attending = models.NullBooleanField(default=None)
    meal = models.CharField(max_length=20, choices=MEALS, null=True, blank=True)
    is_child = models.BooleanField(default=False)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    def __str__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)
