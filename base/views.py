from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.forms import ValidationError

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings

from .models import CustomUser, Box, Comment
from .forms import CustomUserSignUpForm
from .tokens import AccountActivationTokenGenerator, account_activation_token

user = None

def activate(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = CustomUser.objects.get(pk=uid)  
    except:
        user = None
        pass
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.info(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('index') 
    else:  
        messages.info(request, 'Activation link is invalid!')
        return redirect('index')
    
    
def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string(settings.BASE_DIR / 'templates/account_activate_email.html', {
        'user': user.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': AccountActivationTokenGenerator().make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    
    email = EmailMessage(mail_subject, message, to=[to_email])
    
    if email.send():
        messages.info(request, f'Check your {to_email} inbox to activate account')
    else:
        messages.info(request, f"We couldn't send an email with activation email to {to_email}")

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            validate_email(email)
        except ValidationError:
            messages.add_message(request, messages.INFO, f'Email {email} is invalid')
            
            return redirect('index')
        
        if len(password) < 8:
            messages.add_message(request, messages.INFO, 'Password is too short')
            
            return redirect('index')
        
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.add_message(request, messages.INFO, f"There isn't any account created with email {email}")
                    
            return redirect('index')
            

        if user.check_password(password):
            messages.add_message(request, messages.INFO, 'Nice to see you again!')
                    
            if(not request.POST.get('remember')):
                request.session.set_expiry(0)
                
            #ZALOGOWANO 
            print('zalogowano')  
                    
            return redirect('index')
        else:
            messages.add_message(request, messages.INFO, 'Wrong password')
                    
            return redirect('index')       
            
    return render(request, 'index.html')


def sign_up(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password1')
        
        try:
            validate_email(email)
        except ValidationError:
            messages.add_message(request, messages.INFO, f'Email {email} is invalid')
            
            return redirect('sign_up')
        
        if len(password) < 8:
            messages.add_message(request, messages.INFO, 'Password is too short')
            
            return redirect('sign_up')
             
        try:
            form = CustomUserSignUpForm(request.POST)
        
            user = form.save(commit=False)
            user.is_active = False
            user.save()
                
            activateEmail(request, user, email)
            
            return redirect('index')
            
        except ValidationError:
            messages.add_message(request, messages.INFO, 'An errror has occured, try again')
            
            return redirect('sign_up')
    
    else:
        form = CustomUserSignUpForm() 
        
        context = {'form': form} 
    
    return render(request, 'sign_up.html', context)

# def sign_up(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         try:
#             validate_email(email)
#         except ValidationError:
#             messages.add_message(request, messages.INFO, f'Email {email} is invalid')
            
#             return redirect('sign_up')
        
#         if len(password)<6:
#             messages.add_message(request, messages.INFO, 'Password is too short')
            
#             return redirect('sign_up')     
            
#         try:                
#             CustomUser.objects.create_user(email=email,
#                                        password=password,
#                                        nick=request.POST.get('nick')) 
            
#             messages.add_message(request, messages.INFO, 'You signed up successfully!')
            
#             return redirect('index')
        
#         except IntegrityError:
#             messages.add_message(request, messages.INFO, f'User {email} alredy exist, try to log in')
            
#             return redirect('sign_up')         
    
#     return render(request, 'sign_up.html')
