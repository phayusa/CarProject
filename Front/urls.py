from django.conf.urls import url
from views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', index),
    url(r'^about$', about),
    url(r'^404', not_found),
    url(r'^register', register),
    url(r'^prices', prices),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = not_found