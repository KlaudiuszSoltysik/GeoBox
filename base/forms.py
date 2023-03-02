from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import password_validation

from .models import CustomUser


class CustomUserSignUpForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email', 'id': 'email-input'}))
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
