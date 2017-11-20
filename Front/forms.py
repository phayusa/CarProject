# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils import timezone

from Back_Source.models.booking import Booking


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

