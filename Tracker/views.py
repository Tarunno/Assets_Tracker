from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import json

from django.contrib.auth.models import User


@api_view(['GET'])
def ApiOverView(request):
    api_urls = {
        'Sign up': '/users/signup'
    }
    return Response(api_urls)


@api_view(['POST'])
def Signup(request):
    if request.method == 'POST':
        print(json.loads(request.body))
        return Response({'msg': 'user signup'})



