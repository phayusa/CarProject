# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm

from Back_Source.models.booking import Booking, BookingPartner
from Back_Source.models.location import Airport
from Back_Source.models.person import Client, Driver, Commercial, BuissnessPartner


class PersonForm(ModelForm):
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
            ('Inactif', 'Inactif'),
            ('Mail non confirmé', 'Mail non confirmé'),
            ('Actif', 'Actif'),
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

    user = forms.ModelChoiceField(label='Utilisateur', queryset=User.objects.all().order_by("username"), required=False)

    #
    # def clean_status(self):
    #     cleaned_data = super(PersonForm, self).clean()
    #     status = cleaned_data.get("status", None)
    #     if status is 'Inactif':
    #         return status
    #     elif status is 'Mail non confirmé':
    #         return status
    #     elif status is 'Actif':
    #         return status
    #     else:
    #         raise forms.ValidationError("Status n\'est pas valable")
    #
    # def clean_gender(self):
    #     cleaned_data = super(PersonForm, self).clean()
    #     gender = cleaned_data.get("gender", None)
    #     if gender is 'Homme':
    #         return gender
    #     elif gender is 'Femme':
    #         return gender
    #     else:
    #         raise forms.ValidationError("Genre n\'est pas valable")

    def clean(self):
        cleaned_data = super(PersonForm, self).clean()
        username = cleaned_data.get('username', None)
        password = cleaned_data.get('password', None)
        password_confirm = cleaned_data.get('password_bis', None)

        user_select = cleaned_data.get('user', None)
        # print username
        # print user_select
        if not username:
            if not user_select:
                raise forms.ValidationError('Il faut choisir un utilisateur ou en crée un nouveau')
            cleaned_data["user"] = user_select
            return cleaned_data
        else:
            if user_select:
                raise forms.ValidationError('Il faut soit crée un utilisateur soit en choisir un dans la liste')
            try:
                # print password
                # print password_confirm
                if password is password_confirm:
                    raise forms.ValidationError('Les mot de passes ne sont pas identique')
                cleaned_data["user"] = User.objects.create_user(username=username, password=password,
                                                                email=self.cleaned_data['mail'])
                return cleaned_data
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


class PartenerForm(PersonForm):
    class Meta:
        model = BuissnessPartner
        fields = ['first_name', 'last_name', 'mail', 'phone_number', 'age', 'gender', 'status', 'user',
                  'address', 'name_company', 'type_company', 'tva_number', 'iban_number', 'bic_number']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class BookingForm(ModelForm):
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


class BookingPartenerForm(BookingForm):

    date = forms.DateField()
    time = forms.TimeField()

    class Meta:
        model = BookingPartner
        fields = ["airport", "destination", "client", "passengers", "luggage_number",
                  "flight", "model_choose", "vehicle_choose"]


class AirportForm(ModelForm):
    class Meta:
        model = Airport
        fields = ["address", "location"]
