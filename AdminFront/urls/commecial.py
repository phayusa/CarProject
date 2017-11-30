from django.conf.urls import url

from ..views.commercial import *

urlpatterns = [
    url(r'^$', index),
    url(r'^login/$', login_view),
]