# -*- coding: utf-8 -*-

from django.db import models
from person import Driver
from area import Area
from geoposition.fields import GeopositionField

from django.db import models
from location_field.models.plain import PlainLocationField


class VehicleModel(models.Model):
    # Classical attributes
    brand = models.CharField(max_length=200, verbose_name="Marque")
    model = models.CharField(max_length=200, verbose_name="Modèle")
    year = models.CharField(max_length=4, verbose_name="Année")

    # Seats fields
    child_seat = models.BooleanField(verbose_name="Siège enfant")
    number_place = models.IntegerField(verbose_name="Places")
    luggage_number = models.IntegerField(help_text="Taille du coffre en litre", verbose_name="Volume du coffre")

    # Category of the vehicle
    category = models.CharField(max_length=100, verbose_name="Catégorie")

    doors = models.IntegerField(default=5, verbose_name="Portes")

    # Name of the image
    image_default = models.URLField(null=True, blank=True, verbose_name="Image")

    # Price of this selection car
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.category + ' : ' + self.brand + ' ' + self.model + ' ' + str(self.year)

    class Meta:
        verbose_name = "Modèle de voiture"
        verbose_name_plural = "Modèles de voiture"


# Vehicle information
class Vehicle(models.Model):
    # Model
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, verbose_name="Modèle")

    # Driver of the car
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Chauffeur")

    # std fields
    registration = models.CharField(max_length=9, verbose_name="Immatriculation")
    color = models.CharField(max_length=100, null=True, verbose_name="Couleur")

    # Position fields
    pos = GeopositionField(blank=True, verbose_name="Position")

    # adress = models.CharField(max_length=255)
    # location = PlainLocationField(based_fields=['adress'], zoom=7)

    # File or photos to upload
    insurance = models.FileField(verbose_name="Contrat d'Assurance")
    insurance_card = models.FileField(verbose_name="Carte Verte")
    registration_card = models.FileField(verbose_name="Carte Grise")
    front = models.ImageField(verbose_name="Photo Avant")
    back = models.ImageField(verbose_name="Photo Arrière")

    # Buisness field
    revenues = models.IntegerField(blank=True, null=True, verbose_name="Revenues")

    # Processing attributes
    # Busy car
    empty_places = models.IntegerField(verbose_name="Place disponible")
    empty_luggages = models.IntegerField(verbose_name="Volume disponible pour le coffre")
    travelling = models.BooleanField(default=False, blank=True, verbose_name="En voyage")

    # Link area to car
    area = models.ForeignKey(Area, on_delete=models.CASCADE, default=None, null=True, blank=True,
                             verbose_name="Zone assigné")

    def __str__(self):
        return self.registration

    class Meta:
        verbose_name = "Voiture"
