"""Back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views.booking import BookingCreate, BookingList, BookingDetail
from views.vehicle import VehicleCreate, VehicleList, VehicleDetail
from views.vehicle import VehicleModelList
from views.client import ClientCreate, ClientDetail, ClientList
from views.driver import DriverCreate, DriverDetail, DriverList
from views.travel import TravelCreate, TravelDetail, TravelList

urlpatterns = [
    # bookings URL
    url(r'^bookings/$', login_required(BookingList.as_view())),
    url(r'^booking/create/$', login_required(BookingCreate.as_view())),
    url(r'^booking/(?P<pk>[0-9]+)/$', login_required(BookingDetail.as_view())),

    # vehicle URL
    url(r'^vehicles/$', VehicleList.as_view()),
    url(r'^vehicle/create/$', login_required(VehicleCreate.as_view())),
    # url(r'^vehicle/(?P<pk>[0-9]+)(?P<pk>[0-9]+)/$', VehicleDetail.as_view()),

    # vehicles model URL
    url(r'^models/vehicles/$', VehicleModelList.as_view()),

    # clients URL
    url(r'^clients/$', ClientList.as_view()),
    url(r'^client/create/$', ClientCreate.as_view()),
    url(r'^client/(?P<pk>[0-9]+)/$', login_required(ClientDetail.as_view())),

    # driver URL
    url(r'^drivers/$', login_required(DriverList.as_view())),
    url(r'^driver/create/$', login_required(DriverCreate.as_view())),
    url(r'^driver/(?P<pk>[0-9]+)/$', login_required(DriverDetail.as_view())),

    # travel URL
    url(r'^travels/$', login_required(TravelList.as_view())),
    url(r'^travel/create/$', login_required(TravelCreate.as_view())),
    url(r'^travel/(?P<pk>[0-9]+)/$', login_required(TravelDetail.as_view())),

]
