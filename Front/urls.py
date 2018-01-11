from django.conf.urls import url
from views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = [
                  url(r'^$', index, name='home'),
                  url(r'^about$', about),
                  url(r'^404', not_found),
                  url(r'^register', register),
                  url(r'^login', login),
                  url(r'^prices', prices),
                  url(r'^contact', contact),
                  url(r'^pro', contact_pro),
                  url(r'^booking/create/$', booking_create),
                  url(r'^booking/payment/$', booking_payment),
                  url(r'^booking/succeed/(?P<pk>[0-9]+)/$', login_required(booking_succeed)),
                  url(r'^user/$', login_required(user)),
                  url(r'^user/settings/$', login_required(user_settings)),
                  url(r'^user/cards/', login_required(user_cards)),
                  url(r'^user/bookings/$', login_required(user_bookings)),
                  url(r'^user/booking/(?P<pk>[0-9]+)/delete/$', login_required(user_bookings_delete)),
                  url(r'^account_activation_sent/$', account_activation_sent,
                      name='account_activation_sent'),
                  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                      activate, name='activate'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = not_found
