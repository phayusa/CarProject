from django.conf.urls import url

from Back_Source.views.vehicle import serve_image
from ..views.admin import *

urlpatterns = [
    url(r'^$', index),
    # url(r'^login/$', login_view),
    url(r'^areas/$', areas),
    url(r'^map/$', map_view),
    url(r'^manager/$', base_manager),
    url(r'^bookings/$', booking_manager),
    url(r'^cars/$', car_manager),
    # url(r'^clients/$', client_manager),

    # edit url
    url(r'^client/(?P<pk>[0-9]+)/$', client_edit),
    url(r'^driver/(?P<pk>[0-9]+)/$', driver_edit),
    url(r'^commercial/(?P<pk>[0-9]+)/$', commercial_edit),
    url(r'^partener/(?P<pk>[0-9]+)/$', partener_edit),
    url(r'^booking/(?P<pk>[0-9]+)/$', booking_edit),
    url(r'^airport/(?P<pk>[0-9]+)/$', airport_edit),
    url(r'^car-model/(?P<pk>[0-9]+)/$', car_model_edit),
    url(r'^car/(?P<pk>[0-9]+)/$', car_edit),

    # create URL
    url(r'^client/create/$', client_create),
    url(r'^driver/create/$', driver_create),
    url(r'^commercial/create/$', commercial_create),
    url(r'^partener/create/$', partener_create),
    url(r'^car-model/create/$', car_model_create),
    url(r'^car/create/$', car_create),
    url(r'^car/[0-9]+/(?P<image>[A-Za-z0-9\-\_\ .]+)$', serve_image),
    # url(r'^drivers/$', driver_manager),
]
