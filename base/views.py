from django.shortcuts import render
from django.contrib import messages
import pyrebase

from .models import User

config = {
    'apiKey': "AIzaSyBo3eh1dNu2YEiglvDhFIRaoTO6zSqbU_Q",
    'authDomain': "geobox-76fd5.firebaseapp.com",
    'databaseURL': "",
    'projectId': "geobox-76fd5",
    'storageBucket': "geobox-76fd5.appspot.com",
    'messagingSenderId': "488346046244",
    'appId': "1:488346046244:web:c276a2e255f3b8d1672db1"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def index(request):
    return render(request, 'index.html')

def sign_up(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nick = request.POST.get('nick')
        
        try:
            auth.create_user_with_email_and_password(email, password)
            
            User.objects.create(email=email, nick=nick)
            
            messages.add_message(request, messages.INFO, 'You signed up successfully!')
        except:
            messages.add_message(request, messages.INFO, 'Something went wrong.')
    
    return render(request, 'sign_up.html')
