from __future__ import unicode_literals
import datetime
import uuid

from django.db import models
from django.dispatch import receiver

from email_tracker.signals import tracker_opened

# these will determine the default formality of correspondence
ALLOWED_TYPES = [
    ('formal', 'formal'),
    ('fun', 'fun'),
    ('dimagi', 'dimagi'),
]


def _random_uuid():
    return uuid.uuid4().hex


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    type = models.CharField(max_length=10, choices=ALLOWED_TYPES)
    category = models.CharField(max_length=20, null=True, blank=True)
    save_the_date_sent = models.DateTimeField(null=True, blank=True, default=None)
    save_the_date_opened = models.DateTimeField(null=True, blank=True, default=None)
    invitation_id = models.CharField(max_length=32, db_index=True, default=_random_uuid)
    invitation_sent = models.DateTimeField(null=True, blank=True, default=None)
    invitation_opened = models.DateTimeField(null=True, blank=True, default=None)
    is_invited = models.BooleanField(default=False)
    is_attending = models.NullBooleanField(default=None)

    def __unicode__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('category', '-is_invited', 'name')


MEALS = [
    ('beef', 'cow'),
    ('chicken', 'chicken'),
    ('vegetarian', 'vegetable'),
]


class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey(Party)
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
        return u'{}-{}'.format(self.party.invitation_id, self.pk)

    def __unicode__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)


# define signals in models to ensure they are imported
@receiver(tracker_opened)
def track_invitation_opened_signal_catcher(sender, tracking_category, tracking_id, **kwargs):
    if tracking_category == 'invitation-opened':
        track_invitation_opened(tracking_id)


def track_invitation_opened(tracking_id):
    try:
        party = Party.objects.get(invitation_id=tracking_id)
    except Party.DoesNotExist:
        pass
    else:
        party.invitation_opened = datetime.datetime.utcnow()
        party.save()
