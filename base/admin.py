from django.contrib import admin
from .models import User, Box, Comment

admin.site.register(User)
admin.site.register(Box)
admin.site.register(Comment)