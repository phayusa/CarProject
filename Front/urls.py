from django.conf.urls import url
from views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', index),
    url(r'^about$', about),
    url(r'^404', not_found),
    url(r'^register', register),
    url(r'^login', login),
    url(r'^prices', prices),
    url(r'^contact', contact),
    url(r'^booking/$', login_required(booking)),
    url(r'^booking/create/$', booking_create),
    url(r'^booking/succeed/(?P<pk>[0-9]+)/$', login_required(booking_succeed)),
    url(r'^user/$', login_required(user)),
    url(r'^user/settings/$', login_required(user_settings)),
    url(r'^user/bookings/$', login_required(user_bookings)),
    url(r'^user/booking/(?P<pk>[0-9]+)/delete/$', login_required(user_bookings_delete)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = not_found