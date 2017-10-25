from django.conf.urls import url
from django.views.generic import TemplateView
from views import mapView, mapView2, set_driver


urlpatterns = [
    url(r'^map/$', TemplateView.as_view(template_name="map.html"), name="map"),
    url(r'^map2/$', mapView, name="map"),
    url(r'^map22/$', mapView2, name="map"),
    url(r'^drivers/$', set_driver, name="send_driver")
]
