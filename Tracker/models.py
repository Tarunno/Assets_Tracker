from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, is_company, password=None, password2=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            is_company=is_company
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, is_company, password):
        user = self.create_user(username,
            password=password,
            is_company=is_company
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='Username',
        max_length=255,
        unique=True,
    )
    is_company = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['is_company']

    def __str__(self):            
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Device(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Thread(models.Model):
    # Thread will track the assignment and return of devices from a company to a employee

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(max_length=250)
    assigned = models.BooleanField(default=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        if self.assigned == True and self.returned != True:
            return self.employee.company.name + ' assigned ' + self.device.name + ' to ' + self.employee.name + ' at ' + str(self.created_at)
        elif self.assigned == True and self.returned == True:
            return self.employee.name + ' returned ' + self.device.name + ' to ' + self.employee.company.name + ' at ' + str(self.created_at)
    