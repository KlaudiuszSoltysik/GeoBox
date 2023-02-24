from django.db import models

class User(models.Model):   
    email = models.CharField('Email', max_length=64)
    nick = models.CharField('Nick', max_length=64)
    
    def __str__(self):
            return self.email