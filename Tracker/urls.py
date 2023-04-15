from django.urls import path
from .views import *

urlpatterns = [
    path('', ApiOverView, name='api-overview'),
    path('signup/', Signup, name='signup'),
    path('login/', Login, name='login'),
    path('employees/', Employees, name='employees'),
    path('devices/', Devices, name='devices'),
    path('assign/', Assign, name='assign'),
    path('return/<str:device_name>/', Return, name='return'),
    path('threads/', Threads, name='threads'),
]