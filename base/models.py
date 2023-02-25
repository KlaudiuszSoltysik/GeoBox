from django.db import models

class User(models.Model):   
    email = models.EmailField(max_length=64)
    nick = models.CharField(max_length=64)
    
    def __str__(self):
            return self.email
        
class Box(models.Model):   
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
            return self.comment