from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from Tracker.models import *

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ["username", "password", "password2", "is_company"]

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords doesn't match")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create(
            username=validated_data['username'], 
            password=make_password(validated_data['password']),
            is_company=validated_data['is_company']
        )
    
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    is_company = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'is_company']

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread 
        fields = ['employee', 'device', 'condition']