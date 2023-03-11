from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import PasswordResetForm

from crispy_forms.helper import *
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

from .models import CustomUser, Box


class CustomUserSignUpForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    nick = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your nickname'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password2 = None

    class Meta:
        model = CustomUser
        fields = ('email', 'nick', 'password1')
    
    
class CustomUserLogInForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1')

class CustomUserPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    
    class Meta:
        model = CustomUser
        fields = ('email')
    
    
class CustomUserSetPasswordForm(forms.Form):        
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password2 = None
    
    class Meta:
        model = CustomUser
        fields = ('password1')
        
        
class AddBoxForm(forms.ModelForm):
    DIFFICULTY =(
    ('1', '★'),
    ('2', '★★'),
    ('3', '★★★'),
    ('4', '★★★★'),
    ('5', '★★★★★'))
    
    name = forms.CharField(label='Box name', widget=forms.TextInput(attrs={'placeholder': 'Box name'}))
    lat = forms.FloatField(label='Latitude', min_value=-90, max_value=90, widget=forms.NumberInput(attrs={'placeholder': 'Box latitude'}))
    lon = forms.FloatField(label='Longitude', min_value=-90, max_value=90, widget=forms.NumberInput(attrs={'placeholder': 'Box longitude'}))
    img1 = forms.ImageField(label='Tip image', widget=forms.FileInput())
    img2 = forms.ImageField(label='Optional tip image', required=False, widget=forms.FileInput())
    difficulty = forms.ChoiceField(label='Difficulty level', choices=DIFFICULTY, widget=forms.RadioSelect(attrs={'placeholder': 'Difficulty level'}))
    description = forms.CharField(label='Box description', required=False, widget=forms.Textarea(attrs={'placeholder': 'Box description'}))
        
    class Meta:
        model = Box
        fields = ('name', 'lat', 'lon', 'img1', 'img2', 'difficulty', 'description')
        

class FilterForm(forms.Form):
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'placeholder': 'City'}))
    radius = forms.IntegerField(label='Radius', widget=forms.NumberInput(attrs={'placeholder': 'Radius'}))