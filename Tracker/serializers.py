from rest_framework import serializers
from Tracker.models import *

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ["username", "password", "password2", "is_company"]

    def validate(self, attrs):
        name = attrs.get('name')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords doesn't match")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create(
            username=validated_data['username'], 
            password=validated_data['password'],
            is_company=validated_data['is_company']
        )
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_company']