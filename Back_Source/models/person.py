# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from location_field.models.plain import PlainLocationField


# Information for a person as driver or client
class Person(models.Model):
    first_name = models.CharField(max_length=200, verbose_name="Nom")
    last_name = models.CharField(max_length=200, verbose_name="Prénom")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(max_length=10, verbose_name="Sexe")
    mail = models.EmailField(blank=True)
    phone_number = PhoneNumberField(verbose_name="Téléphone")
    user = models.OneToOneField(User, verbose_name="Utilisateur")

    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adresse")
    location = PlainLocationField(blank=True, null=True, based_fields=['address'], zoom=7)

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    class Meta:
        abstract = True

        permissions = (
            ("can_see_its_booking", "Can drive"),
        )


# Client information
class Client(Person):
    payment = models.CharField(max_length=5, blank=True, verbose_name="Type de Payement")


# Driver information
class Driver(Person):
    revenues = models.IntegerField(default=0, blank=True, null=True, verbose_name="Revenues")
    remuneration = models.IntegerField(default=0, blank=True, null=True, verbose_name="Rémunération")

    class Meta:
        verbose_name = "Chauffeur"


# Commercial information
class Commercial(Person):
    revenues = models.IntegerField(default=0, blank=True, null=True, verbose_name="Revenues")
    remuneration = models.IntegerField(default=0, blank=True, null=True, verbose_name="Rémunération")

    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commerciaux"


# Partership information
class BuissnessPartner(Person):
    name_company = models.CharField(max_length=500, verbose_name="Nom Société")
    type_company = models.CharField(max_length=500, verbose_name="Forme Juridique")
    tva_number = models.CharField(max_length=500, verbose_name="Numéro TVA")

    # Payment information
    iban_number = models.CharField(max_length=500, verbose_name="IBAN")
    bic_number = models.CharField(max_length=500, verbose_name="BIC")

    class Meta:
        verbose_name = "Partenaire Commercial"
        verbose_name_plural = "Partenaire Commerciaux"
