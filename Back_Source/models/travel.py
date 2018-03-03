# -*- coding: utf-8 -*-

from django.db import models

from area import Area
from booking import Booking
from location import Airport
from person import Driver
from vehicle import Vehicle


# One travel did by multiples clients link to one car
class Travel(models.Model):
    # Filled once the travel have all people
    car = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Voiture")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Chauffeur")

    # Fill during the attribution of driver
    bookings = models.ManyToManyField(Booking, blank=True, verbose_name="Réservations")

    # The date to the depart
    start = models.DateTimeField(blank=True, null=True, verbose_name="Départ Prévue")
    # The date to the estimated return
    end = models.DateTimeField(blank=True, null=True, verbose_name="Arrivée")

    # Number of passengers can be in the travel (in case of 8 car places)
    free_place = models.IntegerField(default=0, verbose_name="Nombre de places disponible")

    # Area for the travel destination
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="Zone")
    # Starting point of the airport
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name="Aéroport de départ")

    # know if already made or not
    done = models.BooleanField(default=False, verbose_name="Réalisé")

    def __unicode__(self):
        return u'%s - %s - %s' % (self.start, self.airport, self.area)

    class Meta:
        verbose_name = "Trajet"
