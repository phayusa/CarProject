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
from views.booking import BookingCommercialList, BookingPartenerList
from views.vehicle import VehicleCreate, VehicleList, VehicleDetail
from views.vehicle import VehicleModelList, serve_image, serve_vehicle_driver, VehicleDriverSetter
from views.client import ClientCreate, ClientDetail, ClientList
from views.commercials import CommercialList, CommercialDetail, CommercialCreate
from views.parteners import PartenerList, PartenerDetail, PartenerCreate
from views.driver import DriverCreate, DriverDetail, DriverList, DriverBookings
from views.travel import TravelCreate, TravelDetail, TravelList
from views.airport import AirportList, AirportCreate, AirportDetail

urlpatterns = [
    # bookings URL
    url(r'^bookings/$', login_required(BookingList.as_view())),
    url(r'^booking/create/$', login_required(BookingCreate.as_view())),
    url(r'^booking/(?P<pk>[0-9]+)/$', login_required(BookingDetail.as_view())),

    # bookings commecial URL
    url(r'^bookings-commercials/$', login_required(BookingCommercialList.as_view())),

    # bookings URL
    url(r'^bookings-parteners/$', login_required(BookingPartenerList.as_view())),

    # vehicle URL
    url(r'^vehicles/$', VehicleList.as_view()),
    # url(r'^vehicle/create/$', login_required(VehicleCreate.as_view())),
    url(r'^vehicle/(?P<pk>[0-9]+)/driver/$', VehicleDriverSetter.as_view()),
    # url(r'^vehicle/(?P<pk>[0-9]+)(?P<pk>[0-9]+)/$', VehicleDetail.as_view()),

    # vehicles model URL
    url(r'^models/vehicles/$', VehicleModelList.as_view()),
    url(r'^vehicles/(?P<image>[A-Za-z0-9\-\_\ .]+)$', serve_image),

    # clients URL
    url(r'^clients/$', ClientList.as_view()),
    # url(r'^client/create/$', ClientCreate.as_view()),
    url(r'^client/(?P<pk>[0-9]+)/$', login_required(ClientDetail.as_view())),

    # commercial URL
    url(r'^commercials/$', CommercialList.as_view()),
    # url(r'^commercial/create/$', CommercialCreate.as_view()),
    # url(r'^commercial/(?P<pk>[0-9]+)/$', login_required(CommercialDetail.as_view())),

    # partener URL
    url(r'^parteners/$', PartenerList.as_view()),
    # url(r'^partener/create/$', PartenerCreate.as_view()),
    # url(r'^partener/(?P<pk>[0-9]+)/$', login_required(PartenerDetail.as_view())),

    # driver URL
    url(r'^drivers/$', login_required(DriverList.as_view())),
    # url(r'^driver/create/$', login_required(DriverCreate.as_view())),
    url(r'^driver/(?P<pk>[0-9]+)/$', login_required(DriverDetail.as_view())),
    url(r'^driver/travel/$', DriverBookings.as_view()),

    # travel URL
    url(r'^travels/$', TravelList.as_view()),
    url(r'^travel/create/$', login_required(TravelCreate.as_view())),
    url(r'^travel/(?P<pk>[0-9]+)/$', login_required(TravelDetail.as_view())),

    # Airport URL
    url(r'^airports/$', AirportList.as_view()),
    url(r'^airport/create/$', login_required(AirportCreate.as_view())),
    url(r'^airport/(?P<pk>[0-9]+)/$', login_required(AirportDetail.as_view())),

]
