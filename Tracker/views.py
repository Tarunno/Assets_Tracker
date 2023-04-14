from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
import json

from Tracker.serializers import *
from Tracker.models import *
from Tracker.renderers import *

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['GET'])
def ApiOverView(request):
    api_urls = {
        'Signup': '/signup',
        'Login': '/login'
    }
    return Response(api_urls)


@api_view(['POST'])
@renderer_classes([UserRenderer])
def Signup(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  
          user = serializer.save()
          token = get_tokens_for_user(user)
          if serializer.data['is_company']:
              Company.objects.create(user=user, name=serializer.data['username'])
          return Response({'msg': 'Registration successful', 'token':token})
        else: return Response(serializer.errors)
        

@api_view(['POST'])
@renderer_classes([UserRenderer])
def Login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            is_company = serializer.data.get('is_company')
            
            user = authenticate(username=username, password=password)
            if user is not None and user.is_company == is_company:  
                token = get_tokens_for_user(user)
                return Response({'msg': 'Login successful', 'token':token})
            else: return Response({'msg': 'Invalid user or company'})
                


@api_view(['GET'])
@renderer_classes([UserRenderer])
@permission_classes([IsAuthenticated])
def Employees(request):
    user = request.user
    if user.is_company:
      company = user.company_set.first()
      employees = [i.name for i in company.employee_set.only('name').all()]
      print(employees)
      return Response({
          'msg':{
            "employess": employees,
            "company": company.name
          }
      })
    else:
      return Response({'msg':'Only companies have access to employee list'})
