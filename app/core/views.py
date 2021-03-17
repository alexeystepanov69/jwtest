from datetime import datetime
import requests
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from core.serializers import UserSerializer

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


# Create your views here.
class CreateUserAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ObtainJWTCookie(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            token = serializer.object.get('token')
            response = requests.get('https://bitest.sbermarketing.ru/jwt/hub/',
                                    headers={'Authorization': 'Bearer' + token})
            auth_cookie = response.cookies.get(api_settings.JWT_AUTH_COOKIE)
            redirected_response = redirect(to='https://bitest.sbermarketing.ru/jwt/hub/')
            expiration = (datetime.utcnow() +
                          api_settings.JWT_EXPIRATION_DELTA)
            redirected_response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                           auth_cookie,
                                           domain='.sbermarketing.ru',
                                           expires=expiration,
                                           httponly=True)
            return redirected_response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)