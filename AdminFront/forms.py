# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils import timezone

from Back_Source.models.person import Client, Driver, Commercial, BuissnessPartner


class ClientForm(ModelForm):
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

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status', 'user',
                  'address']


class DriverForm(ModelForm):
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

    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status', 'user',
                  'address']


class CommercialForm(ModelForm):
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

    class Meta:
        model = Commercial
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status', 'user',
                  'address']


class PartenerForm(ModelForm):
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

    class Meta:
        model = BuissnessPartner
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status', 'user',
                  'address', 'name_company', 'type_company', 'tva_number', 'iban_number', 'bic_number']