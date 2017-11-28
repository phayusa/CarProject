# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User

from Back_Source.models.person import Client, Driver, Commercial, BuissnessPartner
from Back_Source.models.booking import Booking
from Back_Source.models.location import Airport
from location_field.models.plain import PlainLocationField


class PersonForm(ModelForm):
    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ('homme', 'Homme'),
            ('femme', 'Femme'),
        )
    )

    status = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ('inactif', 'Inactif'),
            ('mail non confirmé', 'Mail non confirmé'),
            ('actif', 'Actif'),
        )
    )

    mail = forms.EmailField()

    age = forms.NumberInput()


class ClientForm(PersonForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status', 'user',
                  'address']


class DriverForm(PersonForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status', 'user',
                  'address']


class CommercialForm(PersonForm):
    class Meta:
        model = Commercial
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status', 'user',
                  'address']


class PartenerForm(ModelForm):
    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ('Homme', 'Homme'),
            ('Femme', 'Femme'),
        )
    )

    status = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ('inactif', 'Inactif'),
            ('mail non confirmé', 'Mail non confirmé'),
            ('actif', 'Actif'),
        )
    )

    mail = forms.EmailField()

    age = forms.NumberInput()

    class Meta:
        model = BuissnessPartner
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status', 'user',
                  'address', 'name_company', 'type_company', 'tva_number', 'iban_number', 'bic_number']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class BookingForm(ModelForm):
    # pasengers = forms.ChoiceField(
    #     widget=forms.RadioSelect,
    #     choices=(
    #         ('homme', 'Homme'),
    #         ('femme', 'Femme'),
    #     )
    # )
    passengers = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Passagers")

    luggage_number = forms.ChoiceField(choices=[(i, i) for i in range(1, 5)], label="Baggages")

    status = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ('En cours de validation', 'En cours de validation'),
            ('Chauffeur choisit', 'Chauffeur choisit'),
            ('Effectué', 'Effectué'),
        )
    )

    class Meta:
        model = Booking
        fields = ["airport", "destination", "client", "passengers", "luggage_number",
                  "flight", "arrive_time", "model_choose", "vehicle_choose", "status"]


class AirportForm(ModelForm):

    class Meta:
        model = Airport
        fields = ["address", "location"]
