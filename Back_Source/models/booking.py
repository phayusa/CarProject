# -*- coding: utf-8 -*-

from django.db import models
from person import Client, Commercial, BuissnessPartner, Operator
from location import Airport
from vehicle import Vehicle
from vehicle import VehicleModel
from geoposition.fields import GeopositionField
from location_field.models.plain import PlainLocationField


# One booking made by a client
class Booking(models.Model):
    # departure = GeopositionField(verbose_name="Position du départ")
    # destination = GeopositionField(verbose_name="Position de la destination")

    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name="Aéroport")
    destination = models.CharField(max_length=255)
    destination_location = PlainLocationField(based_fields=['destinations'], zoom=7)

    date = models.DateField(auto_now=True, verbose_name="Date Réservation")
    # travel = models.ForeignKey(Travel, on_delete=models.CASCADE, null=True)

    # Information about persons
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    passengers = models.IntegerField(verbose_name="Nombre de passagers")
    luggage_number = models.IntegerField(verbose_name="Nombre de baggages")
    child_seat = models.BooleanField(verbose_name="Siège enfant", default=False)

    # Flight info
    flight = models.CharField(max_length=200, verbose_name="Vol")
    arrive_time = models.DateTimeField(blank=True, verbose_name="Date d\'Arrivée")

    # Wanted model
    model_choose = models.ForeignKey(VehicleModel, blank=True, null=True, verbose_name="Modèle souhaitée")

    # Processing value
    vehicle_choose = models.ForeignKey(Vehicle, blank=True, null=True, verbose_name="Voiture")

    # To know the nth booking selected for the travel
    distance = models.IntegerField(blank=True, null=True, verbose_name="Distance Départ-Destination")
    time_estimated = models.IntegerField(verbose_name="Temps estimé en secondes")

    status = models.CharField(max_length=100, default="Ajout dans panier")

    account = models.IntegerField(default=5, verbose_name="Accompte")
    accountType = models.CharField(max_length=5, default="CB", verbose_name="Réglement de l'accompte")

    # Fill by the driver after the travel
    payement_type = models.CharField(max_length=5, default="Aucun")

    def __str__(self):
        return str(self.client) + ' ' + self.date.strftime('%m/%d/%Y') + ' for ' + self.arrive_time.strftime(
            '%m/%d/%Y %Hh%M')

    class Meta:
        verbose_name = u'Réservation'


# Booking made by operator; Payment are made on agency
class BookingOperator(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name="Aéroport")
    destination = models.CharField(max_length=255)
    destination_location = PlainLocationField(based_fields=['destinations'], zoom=7)

    date = models.DateField(auto_now=True, verbose_name="Date Réservation")
    # travel = models.ForeignKey(Travel, on_delete=models.CASCADE, null=True)

    # Information about persons
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    passengers = models.IntegerField(verbose_name="Nombre de passagers")
    luggage_number = models.IntegerField(verbose_name="Nombre de baggages")

    # Flight info
    flight = models.CharField(max_length=200, verbose_name="Vol")
    arrive_time = models.DateTimeField(blank=True, verbose_name="Date d\'Arrivée")

    # Wanted model
    model_choose = models.ForeignKey(VehicleModel, blank=True, null=True, verbose_name="Modèle souhaitée")

    # Processing value
    vehicle_choose = models.ForeignKey(Vehicle, blank=True, null=True, verbose_name="Voiture")
    # To know the nth booking selected for the travel
    distance = models.IntegerField(blank=True, null=True, verbose_name="Distance Départ-Destination")
    time_estimated = models.IntegerField(verbose_name="Temps estimé en secondes")

    status = models.CharField(max_length=100, default="En cours de validation")

    # Fill by the driver after the travel
    payement_type = models.CharField(max_length=5, default="Aucun")

    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.client) + ' ' + self.date.strftime('%m/%d/%Y') + ' for ' + self.arrive_time.strftime(
            '%m/%d/%Y %Hh%M')

    class Meta:
        verbose_name = u'Réservation Opérateur'
        verbose_name_plural = u'Réservations Opérateur'


class BookingCommecial(Booking):
    commercial = models.ForeignKey(Commercial, on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Réservation Commercial'
        verbose_name_plural = u'Réservations Commercial'


class BookingPartner(Booking):
    partner = models.ForeignKey(BuissnessPartner, on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Réservation Partenaire'
        verbose_name_plural = u'Réservations Partenaire'
