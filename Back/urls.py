"""Back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^base-admin/', admin.site.urls),
    url(r'^admin/', include('AdminFront.urls.admin')),
    url(r'^partener/', include('AdminFront.urls.partener')),
    url(r'^commercial/', include('AdminFront.urls.commecial')),
    url(r'^db/', include('Back_Source.urls')),
    url(r'^localisation/', include('Localisation.urls')),
    url(r'^user/', include('Connections.urls')),
    url(r'^user/', include('Connections.urls')),
    url(r'^', include('Front.urls')),
]
