from __future__ import unicode_literals

from django.db import models


class Guest(models.Model):

    name = models.TextField()
    email = models.TextField()
    save_the_date_sent = models.BooleanField(default=False)
    save_the_date_opened = models.BooleanField(default=False)
    invited = models.BooleanField(default=False)
    attending = models.NullBooleanField(default=None)

    def __unicode__(self):
        return self.name
