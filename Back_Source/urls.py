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
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token

from Connections.views.user import LoginView, logout_android
from views.airport import AirportList, AirportCreate, AirportDetail
from views.booking import BookingCommercialList, BookingPartenerList
from views.booking import BookingCreate, BookingList, BookingDetail
from views.booking import BookingOperatorList
from views.client import ClientDetail, ClientList
from views.commercials import CommercialList
from views.driver import DriverDetail, DriverList, DriverBookings
from views.parteners import PartenerList
from views.travel import TravelCreate, TravelDetail, TravelList
from views.vehicle import VehicleList, VehicleDetail, VehicleListJson
from views.vehicle import VehicleModelList, serve_image, VehicleDriverSetter
urlpatterns = [

    # Connection url
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', logout_android),
    url(r'^check/$', verify_jwt_token),
    url(r'^refresh/', refresh_jwt_token),

    # bookings URL
    url(r'^bookings/$', login_required(BookingList.as_view())),
    url(r'^booking/create/$', login_required(BookingCreate.as_view())),
    url(r'^booking/(?P<pk>[0-9]+)/$', BookingDetail.as_view()),

    # bookings commecial URL
    url(r'^bookings-commercials/$', login_required(BookingCommercialList.as_view())),

    # bookings URL
    url(r'^bookings-parteners/$', login_required(BookingPartenerList.as_view())),

    url(r'^bookings-operators/$', login_required(BookingOperatorList.as_view())),

    # vehicle URL
    url(r'^vehicles/$', VehicleList.as_view()),
    url(r'^api/vehicles/$', VehicleListJson.as_view()),
    # url(r'^vehicle/create/$', login_required(VehicleCreate.as_view())),
    url(r'^vehicle/(?P<pk>[0-9]+)/driver/$', VehicleDriverSetter.as_view()),
    url(r'^vehicle/(?P<pk>[0-9]+)/$', VehicleDetail.as_view()),

    # vehicles model URL
    url(r'^models/vehicles/$', login_required(VehicleModelList.as_view())),
    url(r'^vehicles/(?P<image>[A-Za-z0-9\-\_\ .]+)$', serve_image),

    # clients URL
    url(r'^clients/$', login_required(ClientList.as_view())),
    url(r'^client/(?P<pk>[0-9]+)/$', ClientDetail.as_view()),

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
    url(r'^travel/create/$', TravelCreate.as_view()),
    url(r'^travel/(?P<pk>[0-9]+)/$', TravelDetail.as_view()),

    # Airport URL
    url(r'^airports/$', login_required(AirportList.as_view())),
    url(r'^airport/create/$', login_required(AirportCreate.as_view())),
    url(r'^airport/(?P<pk>[0-9]+)/$', AirportDetail.as_view()),

]

