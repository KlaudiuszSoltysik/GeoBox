from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest

from .models import CustomUser, Box, Comment
from .forms import CustomUserSignUpForm, CustomUserLogInForm, CustomUserPasswordResetForm, CustomUserSetPasswordForm, AddBoxForm, FilterForm, AddCommentForm
from .tokens import AccountActivationTokenGenerator, account_activation_token

import pandas as pd
import geopy.distance

# dodać sortowanie
# dadać nawigację do boxa
# my account (boxy, komentarze, edycja, kasowanie)

def log_out(request):
    logout(request)
    request.user = None
    
    messages.add_message(request, messages.INFO, "Now you're logged out.")
    return redirect('index')


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))

    try:
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.info(
            request, 'Thank you for your email confirmation. Now you can login.'
        )
    else:
        messages.info(request, 'Activation link is invalid!')

    return redirect('index')


def reset_password(request):
    log_in_form = CustomUserLogInForm()
    form = CustomUserPasswordResetForm()

    if request.method == 'POST':
        form = CustomUserPasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = CustomUser.objects.get(email=email)
            except:
                messages.info(request, f"We couldn't send an email to {email}.")
                return redirect('reset_password')

            if user:
                mail_subject = 'Reset your password.'
                message = render_to_string(
                    settings.BASE_DIR / 'templates/email/reset_password.html',
                    {
                        'user': user.email,
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http',
                    },
                )

                mail = EmailMessage(mail_subject, message, to=[email])

                if mail.send():
                    messages.info(
                        request, f'Check your {email} inbox to reset your password.'
                    )
                else:
                    messages.info(request, f"We couldn't send an email to {email}.")

                return redirect('index')

            else:
                messages.warning(request, f"User {email} doesn't exist.")
                return redirect('reset_password_email')

    context = {'log_in_form': log_in_form, 
               'form': form,
               'user': None}
    
    return render(request, 'reset_password_email.html', context)


def set_new_password(request, uidb64, token):
    log_in_form = CustomUserLogInForm()
    form = CustomUserSetPasswordForm()

    if request.method == 'POST':
        form = CustomUserSetPasswordForm(request.POST)

        if form.is_valid():
            uid = force_str(urlsafe_base64_decode(uidb64))

            try:
                user = CustomUser.objects.get(pk=uid)
            except:
                user = None

            if user is not None and default_token_generator.check_token(user, token):

                password = form.cleaned_data['password1']

                if len(password) < 8:
                    messages.info(request, 'Invalid password.')
                    return redirect('set_new_password', uidb64=uidb64, token=token)

                user.set_password(password)
                user.save()
                messages.info(request, 'Password resetted. Now you can login.')
            else:
                messages.info(request, 'Reset link is invalid!')

            return redirect('index')
        
    context = {'log_in_form': log_in_form, 
               'form': form,
               'user': None}

    return render(request, 'reset_password_password.html', context)
    
    
def reset_filters(request):
    try:
        del request.session['box_filter']
        del request.session['form_city']
        del request.session['form_radius']
    except:
        pass

   
def get_suggestions(request, input):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            cities = pd.read_csv(settings.BASE_DIR / 'static/cities_db.csv', sep=';')
            cities = cities.loc[cities['Name'].str.startswith(input.title())].sort_values(by='Population', ascending=False).head(5).to_json(force_ascii=False, orient='records')
            
            return JsonResponse({'context': cities})
    else:
        return HttpResponseBadRequest('Invalid request')
    
    
def delete_comment(request, id):
    if request.method == 'DELETE':
        comment = Comment.objects.get(id=id)
            
        if comment.user == request.user:
            comment.delete()
                
        return JsonResponse({'success': 'true'})
    else:
        return HttpResponseBadRequest('Invalid request')

    
def index(request):
    user = None
    
    if request.user.is_authenticated:
        user = request.user

    log_in_form = CustomUserLogInForm()
    
    reset_filters(request)
    
    if request.method == 'POST':
        log_in_form = CustomUserLogInForm(request.POST)

        if log_in_form.is_valid():
            email = log_in_form.cleaned_data['email']
            password = log_in_form.cleaned_data['password1']

            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(2592000)

            user = authenticate(username=email, password=password)
            
            if user:
                login(request, user)
                
                messages.add_message(request, messages.INFO, 'Nice to see you again!')
            else:
                messages.add_message(
                    request, messages.INFO, "We couldn't log in account with that data."
                )
    
    context = {'log_in_form': log_in_form, 
               'user': user,
               'boxes_lat': [box.lat for box in Box.objects.all()],
               'boxes_lon': [box.lon for box in Box.objects.all()],
               'boxes_img': [box.img1 for box in Box.objects.all()],
               'boxes_id': [box.id for box in Box.objects.all()]}

    return render(request, 'index.html', context)


def sign_up(request):
    log_in_form = CustomUserLogInForm()
    form = CustomUserSignUpForm()

    reset_filters(request)
    
    if request.method == 'POST':
        log_in_form = CustomUserLogInForm(request.POST)

        if log_in_form.is_valid():
            email = log_in_form.cleaned_data['email']
            password = log_in_form.cleaned_data['password1']

            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(2592000)

            user = authenticate(username=email, password=password)
            
            if user:
                login(request, user)
                
                messages.add_message(request, messages.INFO, 'Nice to see you again!')
            else:
                messages.add_message(
                    request, messages.INFO, "We couldn't log in account with that data."
                )

    if request.method == 'POST':
        form = CustomUserSignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            mail_subject = 'Activate your user account.'
            message = render_to_string(
                settings.BASE_DIR / 'templates/email/account_activate_email.html',
                {
                    'user': user.email,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': AccountActivationTokenGenerator().make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                },
            )

            mail = EmailMessage(mail_subject, message, to=[email])

            if mail.send():
                messages.info(request, f'Check your {email} inbox to activate account.')
            else:
                messages.info(
                    request,
                    f"We couldn't send an email with activation link to {email}.",
                )

            return redirect('index')
        
    context = {'log_in_form': log_in_form, 
               'form': form,
               'user': None}

    return render(request, 'sign_up.html', context)


def boxes(request):
    user = None
          
    if request.user.is_authenticated:
        user = request.user
    
    log_in_form = CustomUserLogInForm()
    filter_form = FilterForm()

    if request.method == 'POST':
        log_in_form = CustomUserLogInForm(request.POST)

        if log_in_form.is_valid():
            email = log_in_form.cleaned_data['email']
            password = log_in_form.cleaned_data['password1']

            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(2592000)

            user = authenticate(username=email, password=password)
            
            if user:
                login(request, user)
                
                messages.add_message(request, messages.INFO, 'Nice to see you again!')
            else:
                messages.add_message(
                    request, messages.INFO, "We couldn't log in account with that data."
                )
    
    if request.method == 'POST':        
        form = FilterForm(request.POST)

        if form.is_valid():            
            city = form.cleaned_data['city']
            radius = form.cleaned_data['radius']
           
            if city and radius:
                cities = pd.read_csv(settings.BASE_DIR / 'static/cities_db.csv', sep=';')
                
                request.session['form_city'] = city
                request.session['form_radius'] = radius
                
                city_row = cities.loc[cities['Name'] == city.title()]
                
                city_lat, city_lon = str(city_row['Coordinates'].iloc[0]).split(', ')
                
                tmp_box_filter = []
                
                for box in Box.objects.all():
                    if geopy.distance.geodesic((float(city_lat), float(city_lon)), (float(box.lat), float(box.lon))).m <= float(radius):
                        tmp_box_filter.append(box.id)
                
                request.session['box_filter'] = tmp_box_filter
            else:
                request.session['form_city'] = ''
                request.session['form_radius'] = ''
                request.session['box_filter'] = [box.id for box in Box.objects.all()]
        
    if filter := request.session.get('box_filter'):
        boxes = Box.objects.all().filter(id__in=filter).order_by('name')
        form_city = request.session.get('form_city')
        form_radius = request.session.get('form_radius')
    else:
        boxes = Box.objects.all().order_by('name')
        form_city = ''
        form_radius = ''
    
    paginator = Paginator(boxes, 5)
    page = request.GET.get('page')
    boxes = paginator.get_page(page)
    pages_count = boxes.paginator.num_pages
    
    if pages_count < 5:
        page_numbers = range(1, pages_count + 1)
    else:
        if n := boxes.number < 3:
            min = 1
        else:
            min = n - 2
            
        if n := boxes.number > pages_count - 2:
            max = pages_count + 1
        else:
            max = n + 3

        page_numbers = list(range(min, max))
        page_numbers.append('...')
        page_numbers.append(pages_count)  
    
    context = {
        'log_in_form': log_in_form,
        'filter_form': filter_form,
        'user': user,
        'boxes': boxes,
        'page_numbers': page_numbers,
        'form_city': form_city,
        'form_radius': form_radius,
    }

    return render(request, 'boxes.html', context)


@login_required
def add_box(request):
    user = request.user
    
    reset_filters(request)

    log_in_form = CustomUserLogInForm()
    form = AddBoxForm()

    if request.method == 'POST':
        form = AddBoxForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.instance.user = user
                form.save()
                messages.add_message(request, messages.INFO, 'Box added.')
                
                return redirect('boxes')
            except:
                messages.add_message(request, messages.INFO, 'Something went wrong.')

    context = {'log_in_form': log_in_form, 
               'user': user, 
               'form': form}

    return render(request, 'add_box.html', context)


def box(request, id):
    user = None
    
    if request.user.is_authenticated:
        user = request.user
        
    comments = Comment.objects.all().filter(box=id).order_by('-timestamp', )
    
    log_in_form = CustomUserLogInForm()
    form = AddCommentForm()
    
    if request.method == 'POST':
        log_in_form = CustomUserLogInForm(request.POST)

        if log_in_form.is_valid():
            email = log_in_form.cleaned_data['email']
            password = log_in_form.cleaned_data['password1']

            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(2592000)

            user = authenticate(username=email, password=password)
            
            if user:
                login(request, user)
                
                messages.add_message(request, messages.INFO, 'Nice to see you again!')
            else:
                messages.add_message(
                    request, messages.INFO, "We couldn't log in account with that data."
                )
    
    if request.method == 'POST':        
        form = AddCommentForm(request.POST)

        if form.is_valid():
            try:
                form.instance.user = user
                form.instance.box = Box.objects.get(id=id)
                form.save()
                
                return redirect('box', id=id)
            except:
                messages.add_message(request, messages.INFO, 'Something went wrong.')
    
    context = {'log_in_form': log_in_form,
               'user': user,
               'box': Box.objects.get(id=id),
               'comments': comments,
               'form': form}
    
    return render(request, 'box.html', context)
