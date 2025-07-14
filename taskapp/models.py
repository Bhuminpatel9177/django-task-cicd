from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class Register(models.model):
#     first_name = models.CharField(max_length = 20)
#     last_name = models.CharField(max_length = 20)
#     email = models.CharField(max_length = 50, unique=True)
#     mobile = models.CharField(max_length = 10)
#     dob = models.DateField()
#     password = models.CharField(max_length=50)
#     gender = models.CharField(max_length = 10)

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=10, null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    otp= models.CharField(max_length=6, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

class ExtraField(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    hobbies = models.CharField(max_length=50, null=True)
    





