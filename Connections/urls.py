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
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from views.user import LoginView, LogoutView, LoginViewWeb, logout_android, user_authenticate
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/android/$', logout_android),
    url(r'^logout/$', login_required(LogoutView.as_view())),
    url(r'^login_view/$', LoginViewWeb.as_view()),
    url(r'^check/$', verify_jwt_token),
    url(r'^refresh/', refresh_jwt_token),

]
