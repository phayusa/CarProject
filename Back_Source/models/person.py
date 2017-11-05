# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Information for a person as driver or client
class Person(models.Model):
    first_name = models.CharField(max_length=200, verbose_name="Nom")
    last_name = models.CharField(max_length=200, verbose_name="Prénom")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(max_length=10, verbose_name="Sexe")
    mail = models.EmailField(blank=True)
    phone_number = PhoneNumberField(verbose_name="Téléphone")
    user = models.OneToOneField(User, verbose_name="Utilisateur")

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
