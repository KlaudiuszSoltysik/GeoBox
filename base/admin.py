from django.contrib import admin
from .models import CustomUser, Box, Comment

admin.site.register(CustomUser)
admin.site.register(Box)
admin.site.register(Comment)