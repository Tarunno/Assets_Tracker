from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import*

class UserModelAdmin(BaseUserAdmin):
    list_display = ('username', 'is_company', 'is_admin')
    list_filter = ('is_admin', 'is_company')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('is_company',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Device)