from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout,authenticate
from django.template.loader import render_to_string

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from .models import CustomUser
import random


@api_view(['POST',])
def register_view(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['email']
        password = request.POST['password']
        mobile_no = request.POST['mobile_no']
        if not CustomUser.objects.filter(username=username).exists():
            CustomUser.objects.create(name = name,
                                     username=username,
                                     email = username,
                                     user_role = 2,
                                     mobile_no=mobile_no,
                                     password = make_password(password))
            response = {
                'status':200,
                'message': "success",
                'data':{'message':"User Register Successfully!"}
            }
            return Response(response,status=status.HTTP_200_OK)
        else:
            response = {
                'status':400,
                'message': "failed",
                'data':{'message':"User Already Exists !"}
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def login_api(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'status':200,
                    'message': "success",
                    'data':{'message':"Login Successfully!",
                            'token':token.key,
                            'email':user.email,
                            'name':user.name,
                            'mobile_no':user.mobile_no}
                }
                return Response(response,status=status.HTTP_200_OK)

            else:
                response = {
                        'status':400,
                        'message': "failed",
                        'data':{'message':'Invalid Credentials!'}
                    }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                        'status':400,
                        'message': "failed",
                        'data':{'message':'Invalid Credentials!'}
                    }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
