from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_company = models.BooleanField(default=True, null=True, blank=True)


class Company(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Device(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name