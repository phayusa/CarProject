from django.conf.urls import url
from django.views.generic import TemplateView
from views import mapView


urlpatterns = [
    url(r'^map/$', TemplateView.as_view(template_name="map.html"), name="map"),
    url(r'^map2/$', mapView, name="map")
]
