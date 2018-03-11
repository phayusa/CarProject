# -*- coding: utf-8 -*-


from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import *
from Back_Source.models.person import Driver
from Back_Source.models.vehicle import Vehicle
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings


class LoginViewWeb(TemplateView):
    template_name = 'front/index.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permissions_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        array_key = request.POST

        username = array_key.get('username', False)
        password = array_key.get('password', False)

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)

            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return HttpResponseRedirect("/")


# Check if we are on mobile
def is_mobile_app_access(request):
    return (request.META.get('HTTP_REFERER', None) is None) and (request.META.get('HTTP_COOKIE',
                                                                                  None) is None) and (
               request.META.get('HTTP_ORIGIN', None) == 'file://')


# and (request.META.get(
#         'HTTP_X_REQUESTED_WITH', None) == 'your.app.name.here')

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        # if not is_mobile_app_access(request):
        #     return HttpResponse("{}")

        username = request.data.get('username', False)
        password = request.data.get('password', False)

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            driver = Driver.objects.filter(user=user)[0]
            if driver:
                response = {'user': username}
                response.update({'token': token})
                response.update({'fullname': driver.last_name + ' ' + driver.first_name})

                cars = Vehicle.objects.filter(driver=driver)
                if cars:
                    response.update({'car': cars[0].id})
                else:
                    response.update({'car': -1})
                return Response(response, status=status.HTTP_202_ACCEPTED)

        # return HttpResponseRedirect('/')
        # return HttpResponseRedirect('/register')
        return Response(status=status.HTTP_400_BAD_REQUEST)
        # return render(request, self.template_name)

    def get(self, request, **kwargs):
        raise Http404("Page non trouvée")


class LogoutView(TemplateView):
    # template_name = '/'

    def get(self, request, **kwargs):
        logout(request)
        # return render(request, self.template_name)
        return HttpResponseRedirect('/')


def logout_android(request):
    logout(request)
    return HttpResponse("Ok")


def user_authenticate(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')

        else:
            return HttpResponseRedirect('/register/')
    else:
        return HttpResponseRedirect('/register/')
