from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import*

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
          'Company',
          {
            'fields':(
              'is_company',
            )
          }
        )
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Device)