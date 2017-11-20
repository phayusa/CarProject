# -*- coding: utf-8 -*-
from django.db import models
from location_field.models.plain import PlainLocationField


class Airport(models.Model):
    address = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['address'], zoom=7)

    def __unicode__(self):
        return self.address

    class Meta:
        verbose_name = u'Aéroport'
