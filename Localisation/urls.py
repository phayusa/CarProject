from django.conf.urls import url
from django.views.generic import TemplateView
from views import mapView, mapView2, upload_bookings_vehicle, autocomplete


urlpatterns = [
    # url(r'^map/$', TemplateView.as_view(template_name="map.html"), name="map"),
    # url(r'^map2/$', mapView, name="map"),
    # url(r'^complete/$', autocomplete, name="map"),
    # url(r'^map22/$', mapView2, name="map"),
    url(r'^drivers/$', upload_bookings_vehicle, name="send_driver")
]
