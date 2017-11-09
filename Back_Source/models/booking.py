# -*- coding: utf-8 -*-

from django.db import models
from person import Client
from vehicle import Vehicle
from geoposition.fields import GeopositionField


# One booking made by a client
class Booking(models.Model):
    departure = GeopositionField(verbose_name="Position du départ")
    destination = GeopositionField(verbose_name="Position de la destination")

    date = models.DateField(auto_now=True, verbose_name="Date Réservation")
    # travel = models.ForeignKey(Travel, on_delete=models.CASCADE, null=True)

    # Information about persons
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    passengers = models.IntegerField(verbose_name="Nombre de passagers")
    luggage_number = models.IntegerField(verbose_name="Volume des baggages")

    # Flight info
    flight = models.CharField(max_length=200, verbose_name="Vol")
    arrive_time = models.DateTimeField(blank=True, verbose_name="Date Réservé")

    # Processing value
    vehicle_choose = models.ForeignKey(Vehicle, blank=True, null=True, verbose_name="Voiture")
    # To know the nth booking selected for the travel
    distance = models.IntegerField(blank=True, null=True, verbose_name="Distance Départ-Destination")

    def __str__(self):
        return str(self.client) + ' ' + self.date.strftime('%m/%d/%Y') + ' for ' + self.arrive_time.strftime(
            '%m/%d/%Y %Hh%M')

    class Meta:
        verbose_name = u'Réservation'

