from django.conf.urls import url, include
from views import *


urlpatterns = [
    url(r'^$', index),
    url(r'^login/$', login_view),
    url(r'^areas/$', areas),
    url(r'^manager/$', base_manager),
    # url(r'^clients/$', client_manager),
    url(r'^client/(?P<pk>[0-9]+)/$', client_edit),
    url(r'^driver/(?P<pk>[0-9]+)/$', driver_edit),
    url(r'^commercial/(?P<pk>[0-9]+)/$', commercial_edit),
    url(r'^partener/(?P<pk>[0-9]+)/$', partener_edit),
    # url(r'^drivers/$', driver_manager),
]