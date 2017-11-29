# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm
from django.utils import timezone

from Back_Source.models.booking import Booking
from Back_Source.models.person import Client


class BookingForm(ModelForm):
    arrive_time = forms.DateTimeField(initial=timezone.now(), label="Heure d'arrivée", required=True)

    # client = forms.HiddenInput()

    # def clean_arrive_time(self):
    #     my_date = self.cleaned_data['my_date']
    #     my_time = self.cleaned_data['my_time']
    #     my_date_time = ('%s %s' % (my_date, my_time))
    #     my_date_time = datetime.strptime(my_date_time, '%Y-%m-%d %H:%M:%S')
    #     if datetime.now() >= my_date_time:
    #         raise forms.ValidationError(u'Wrong Date or Time! "%s"' % my_date_time)
    #     return my_time
    # def clean_arrive_time(self):
    #     date = self.cleaned_data['arrive_time']
    #     print date
    #     if date < timezone.now():
    #         raise forms.ValidationError("La réservation doit se faire dans le future")
    #     return date

    class Meta:
        model = Booking
        fields = ['arrive_time', 'airport', 'destination', 'passengers', 'luggage_number', 'flight', 'model_choose',
                  'client']


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

    def clean_user(self):
        cleaned_data = super(PersonForm, self).clean()
        username = cleaned_data.get('username', None)
        password = cleaned_data.get('password', None)
        password_confirm = cleaned_data.get('password_bis', None)

        # print username
        # print user_select
        if not username:
            raise forms.ValidationError('Aucun nom d\'utilisateur choisit')
        else:
            try:
                if not password or not password_confirm:
                    raise forms.ValidationError('Aucun Mot de Passe non renseigné')

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
