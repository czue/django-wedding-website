from __future__ import unicode_literals

from django.db import models


# these will determine the default formality of correspondence
ALLOWED_TYPES = [
    ('formal', 'formal'),
    ('fun', 'fun')
]


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    type = models.CharField(max_length=10, choices=ALLOWED_TYPES)
    save_the_date_sent = models.DateTimeField(null=True, default=None)
    save_the_date_opened = models.DateTimeField(null=True, default=None)
    is_invited = models.BooleanField(default=False)
    is_attending = models.NullBooleanField(default=None)

    def __unicode__(self):
        return 'Party: {}'.format(self.name)

class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey(Party)
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField()
    is_attending = models.NullBooleanField(default=None)
    is_child = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)
