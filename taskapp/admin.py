from django.contrib import admin
from taskapp.models import CustomUser
from taskapp.models import ExtraField
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ExtraField)