from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate

from Tracker.serializers import *
from Tracker.models import *


@api_view(['GET'])
def ApiOverView(request):
    api_urls = {
        'Signup': '/signup',
        'Login': '/login'
    }
    return Response(api_urls)


@api_view(['POST'])
def Signup(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  
          user = serializer.save()
          if serializer.data['is_company']:
              Company.objects.create(user=user, name=serializer.data['username'])
          return Response({'msg': 'Registration successful'})
        else: return Response(serializer.errors)
        

@api_view(['POST'])
def Login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        print('===========================')
        if serializer.is_valid():
            print("++++++++++++++++++++++++++++")
            username = serializer.data['username']
            password = serializer.data['password']
            is_company = serializer.data['is_company']
            user = authenticate(username=username, password=password, is_company=is_company)
            if user is not None:  
                return Response({'msg': 'Login successful'})
            else: return Response({'msg': 'Invalid user or company'})
                


