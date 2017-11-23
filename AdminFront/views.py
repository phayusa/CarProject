# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from Back_Source.models import VehicleModel, Airport


# Create your views here.


def index(request):
    return render(request, 'base_pages_ecom_dashboard.html')
