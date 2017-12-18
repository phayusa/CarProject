from django.conf.urls import url

from ..views.operator import *

urlpatterns = [
    url(r'^$', index),
    url(r'^login/$', login_view),
    url(r'^manager/$', base_manager),
    url(r'^bookings/$', booking_manager),
    # url(r'^clients/$', client_manager),

    # edit url
    url(r'^client/(?P<pk>[0-9]+)/$', client_edit),
    url(r'^commercial/(?P<pk>[0-9]+)/$', commercial_edit),
    url(r'^booking/(?P<pk>[0-9]+)/$', booking_edit),

    # create URL
    url(r'^client/create/$', client_create),
    url(r'^commercial/create/$', commercial_create),
    url(r'^booking/create/$', booking_create),
]