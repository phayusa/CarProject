from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=1000)
    north = models.FloatField()
    south = models.FloatField()
    east = models.FloatField()
    west = models.FloatField()

    def __str__(self):
        return self.name

