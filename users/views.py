import requests
from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


# Create your views here.


class RegistrationAPIView(APIView):
    http_method_names = [u'post']

    def post(self, request):
        body = {
            'username': request.data['email'],
            'email': request.data['email'],
            'mobile': request.data['mobile'],
            'password1': request.data['password2'],
            'password2': request.data['password2']
        }

        response = requests.post(
            'http://127.0.0.1:8000/api/v1/rest-auth/registration/',
            json=body
        )

        if response.status_code == status.HTTP_204_NO_CONTENT:
            user = User.objects.get(email=request.data['email'])
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.mobile = request.data['mobile']
            user.save()

            return Response(
                {
                    'message': 'User registered successfully',
                    'success': True,
                    'status': status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        else:
            error_message = response.json().get('error_message', 'Unknown error')
            return Response(
                {
                    'message': 'Registration failed',
                    'error_message': error_message,
                    'success': False,
                    'status': response.status_code
                },
                status=response.status_code
            )