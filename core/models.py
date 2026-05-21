from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    
    ]
    email = models.EmailField(unique=True)   #override email to make it unique
    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=100, choices= GENDER_CHOICES, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)


    USERNAME_FIELD = "email"  # this tells django to use email for login purpose instead of username

    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email
    

    
 


