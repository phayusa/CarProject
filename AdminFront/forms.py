# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm

from Back_Source.models.booking import Booking
from Back_Source.models.location import Airport
from Back_Source.models.person import Client, Driver, Commercial, BuissnessPartner


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

    age = forms.IntegerField(validators=[
        MaxValueValidator(120),
        MinValueValidator(18)
    ])

    username = forms.CharField(max_length=1000, label="Nom d'utilisateur", required=False)

    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de Passe", required=False)
    password_bis = forms.CharField(widget=forms.PasswordInput(), label="Confirmer Mot de Passe", required=False)

    def clean(self):
        cleaned_data = super(PersonForm, self).clean()
        username = cleaned_data.get('username', None)
        password = cleaned_data.get('password', None)
        password_confirm = cleaned_data.get('password_bis', None)

        user_select = cleaned_data.get('user', None)
        if not username:
            if not user_select:
                raise forms.ValidationError('Il faut choisir un utilisateur ou en crée un nouveau')
            user = user_select
        else:
            if user_select:
                raise forms.ValidationError('Il faut soit crée un utilisateur soit en choisir un dans la liste')
            try:
                if password is not password_confirm:
                    raise forms.ValidationError('Les mot de passes ne sont pas identique')
                user = User.objects.create_user(username=username, password=password, email=self.cleaned_data['mail'])
            except Exception as exception:
                raise forms.ValidationError(exception.message)


class ClientForm(PersonForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status',
                  'address', 'user']


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
