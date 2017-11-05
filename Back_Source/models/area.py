# -*- coding: utf-8 -*-
from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=1000, verbose_name="Nom")
    north = models.FloatField(verbose_name="Limite au Nord")
    south = models.FloatField(verbose_name="Limite au Sud")
    east = models.FloatField(verbose_name="Limite à l\'est")
    west = models.FloatField(verbose_name="Limit à l\'ouest")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Zone"

