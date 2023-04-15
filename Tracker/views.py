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
        'Signup': 'signup/',
        'Login': 'login/',
        'Employee List': 'employees/',
        'Devices List': 'devices/',
        'Assign Device': 'assign/',
        'Return Device': 'return/<str:device_name>/',
        'Threads': 'threads/'
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
      employees = [(i.id, i.name) for i in company.employee_set.only('name').all()]
      print(employees)
      return Response({
          'msg':{
            "company": company.name,
            "employess": employees
          }
      })
    else:
      return Response({'msg':'Only companies have access to employee list'})


@api_view(['GET'])
@renderer_classes([UserRenderer])
@permission_classes([IsAuthenticated])
def Devices(request):
    user = request.user
    if user.is_company:
      company = user.company_set.first()
      devices = [(i.id, i.name) for i in company.device_set.all()]
      print(devices)
      return Response({
          'msg':{
            "company": company.name,
            "devices": devices
          }
      })
    else:
      return Response({'msg':'Only companies have access to devices'})
    

@api_view(['POST'])
@renderer_classes([UserRenderer])
@permission_classes([IsAuthenticated])
def Assign(request):
    if request.method == 'POST':
        user = request.user
        if user.is_company:
            employee_name = request.data.get('employee')
            device_name = request.data.get('device')
            company = user.company_set.first()
            try:
                employee = Employee.objects.get(name=employee_name)
            except:
                return Response({'msg': 'Provide valid employee name'})
            device = Device.objects.get(name=device_name)

            if employee.company != company:
                return Response({'msg':"Employee doesn't belong to you company"})
            if device.company != company:
                return Response({'msg':"Device doesn't belong to you company"})

            request.data['employee'] = employee.id
            request.data['device'] = device.id

            try:
                thread = Thread.objects.get(employee=employee)
            except:
                thread = None
            if thread is not None and thread.returned == False:
                return Response({'msg': thread.device.name + ' is currently assigned to ' + thread.employee.name})
            

            
            serializer = ThreadSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                
            return Response({
                'msg': company.name + ' assigned ' + device.name + ' to ' + employee.name
            })
        else:
            return Response({'msg':'Only companies can assign devices'})
        

@api_view(['GET'])
@renderer_classes([UserRenderer])
@permission_classes([IsAuthenticated])
def Return(request, device_name):
    user = request.user
    device = Device.objects.get(name=device_name)
    thread = Thread.objects.get(device=device)

    if thread is not None:
        thread.returned = True
        thread.save()
        if thread.returned == False:
            return Response({'msg': device.name + ' returned successfully'})
        else:
            return Response({'msg': device.name + " deosn't belogn to you"})
            
    return Response({'msg': device.name + " deosn't belogn to you"})


@api_view(['GET'])
@renderer_classes([UserRenderer])
@permission_classes([IsAuthenticated])
def Threads(request):
    user = request.user
    if user.is_company:
        company = Company.objects.get(user=user)
        employees = Employee.objects.filter(company=company)
        threads = []
        for employee in employees:
            thread = Thread.objects.filter(employee=employee).order_by('-created_at')
            for i in thread:
                if i.returned:
                    text = i.employee.name + ' returned ' + i.device.name + ' to ' + company.name + ' at ' + str(i.created_at)
                else:
                    text = company.name + ' assigned ' + i.device.name + ' to ' + i.employee.name  + ' at ' + str(i.created_at)
                threads.append(text)
        print(threads)
        return Response({
            'msg': {
                'Threads': threads
            }
        })
    else:
        return Response({'msg': 'Only companies have access to threads'})