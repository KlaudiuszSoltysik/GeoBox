from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nick = models.CharField('Nickname', max_length=60)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nick']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Box(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=64)
    lat = models.FloatField()
    lon = models.FloatField()
    img1 = models.FileField(upload_to='static/images/user_images')
    img2 = models.FileField(upload_to='static/images/user_images', null=True)
    difficulty = models.IntegerField()
    description = models.CharField(max_length=5000, null=True)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.comment