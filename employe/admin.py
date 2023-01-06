from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class Admin(UserAdmin):
    model = User
    list_display = ('username', 'email','first_name','last_name','is_active',
                    'is_staff', 'is_superuser', 'last_login',)

admin.site.register(User,Admin)
admin.site.register(Employe)
admin.site.register(Appointment)