from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from .models import CustomUser


class CustomUserSignUpForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    nick = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your nickname'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'id': 'password-input'}))
    password2 = None

    class Meta:
        model = CustomUser
        fields = ('email', 'nick', 'password1')
        
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
            
        return password1
    
    
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
    