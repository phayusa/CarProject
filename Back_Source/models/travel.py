# -*- coding: utf-8 -*-

from django.db import models
from vehicle import Vehicle
from person import Driver, Client
from booking import Booking


# One travel did by multiples clients link to one car
class Travel(models.Model):
    car = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Voiture")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Chauffeur")

    # Fill during the attribution of driver
    bookings = models.ManyToManyField(Booking, blank=True, verbose_name="Réservations")

    # Fill before and before the travel
    start = models.DateField(blank=True, null=True, verbose_name="Départ")
    end = models.DateField(blank=True, null=True, verbose_name="Arrivée")

    def __unicode__(self):
        return u'%s - %s' % (self.car, self.driver)

    class Meta:
        verbose_name = "Trajet"



