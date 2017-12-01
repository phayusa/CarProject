from django.conf.urls import url

from ..views.commercial import *

urlpatterns = [
    url(r'^$', index),
    url(r'^(?P<pk>[0-9]+)/', edit_booking),
    url(r'^clients/', clients_list),
]
