from django.urls import path
from .views import *

urlpatterns = [
    path('', ApiOverView, name='api-overview'),
    path('signup/', Signup, name='signup'),
    path('login/', Login, name='login'),
]