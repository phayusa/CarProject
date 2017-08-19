from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import *
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
    permissions_classes = (IsAuthenticated, )

    def post(self, request, **kwargs):
        array_key = request.POST

        username = array_key.get('username', False)
        password = array_key.get('password', False)

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)

            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    template_name = 'front/index.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permissions_classes = (IsAuthenticated, )
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):

        username = request.data.get('username', False)
        password = request.data.get('password', False)

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = {'user': username}
            response.update({'token': token})
            return Response(response, status=status.HTTP_202_ACCEPTED)

            #return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        #return render(request, self.template_name)


class LogoutView(TemplateView):
    template_name = 'front/index.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)


class test(TemplateView):
    template_name = 'front/booking.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name)


