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

from .models import CustomUser, Box, Comment
from .forms import CustomUserSignUpForm, CustomUserLogInForm, CustomUserPasswordResetForm, CustomUserSetPasswordForm, AddBoxForm, FilterForm
from .tokens import AccountActivationTokenGenerator, account_activation_token

import pandas as pd

user = None


def log_in(request):
    global user

    if request.method == "POST":
        log_in_form = CustomUserLogInForm(request.POST)

        if log_in_form.is_valid():
            email = log_in_form.cleaned_data["email"]
            password = log_in_form.cleaned_data["password1"]

            if not request.POST.get("remember"):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(2592000)

            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)

                messages.add_message(request, messages.INFO, "Nice to see you again!")
            else:
                messages.add_message(
                    request, messages.INFO, "We couldn't log in account with that data."
                )

            return redirect("index")


def index(request):
    global user

    log_in_form = CustomUserLogInForm()

    context = {"log_in_form": log_in_form, 
               "user": user}

    if request.method == "POST":
        log_in_form = CustomUserLogInForm(request.POST)

        if log_in_form.is_valid():
            email = log_in_form.cleaned_data["email"]
            password = log_in_form.cleaned_data["password1"]

            if not request.POST.get("remember"):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(2592000)

            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)

                messages.add_message(request, messages.INFO, "Nice to see you again!")
            else:
                messages.add_message(
                    request, messages.INFO, "We couldn't log in account with that data."
                )

            return redirect("index")
        else:
            messages.add_message(
                request, messages.INFO, "We couldn't log in account with that data."
            )
            return redirect("index")

    return render(request, "index.html", context)


def sign_up(request):
    log_in_form = CustomUserLogInForm()
    form = CustomUserSignUpForm()

    context = {"log_in_form": log_in_form, 
               "form": form}

    if request.method == "POST":
        form = CustomUserSignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            mail_subject = "Activate your user account."
            message = render_to_string(
                settings.BASE_DIR / "templates/email/account_activate_email.html",
                {
                    "user": user.email,
                    "domain": get_current_site(request).domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": AccountActivationTokenGenerator().make_token(user),
                    "protocol": "https" if request.is_secure() else "http",
                },
            )

            mail = EmailMessage(mail_subject, message, to=[email])

            if mail.send():
                messages.info(request, f"Check your {email} inbox to activate account.")
            else:
                messages.info(
                    request,
                    f"We couldn't send an email with activation link to {email}.",
                )

            return redirect("index")

    return render(request, "sign_up.html", context)


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
            request, "Thank you for your email confirmation. Now you can login."
        )
    else:
        messages.info(request, "Activation link is invalid!")

    return redirect("index")


def reset_password(request):
    log_in_form = CustomUserLogInForm()
    form = CustomUserPasswordResetForm()

    context = {"log_in_form": log_in_form, 
               "form": form}

    if request.method == "POST":
        form = CustomUserPasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            try:
                user = CustomUser.objects.get(email=email)
            except:
                messages.info(request, f"We couldn't send an email to {email}.")
                return redirect("reset_password")

            if user:
                mail_subject = "Reset your password."
                message = render_to_string(
                    settings.BASE_DIR / "templates/email/reset_password.html",
                    {
                        "user": user.email,
                        "domain": get_current_site(request).domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": "https" if request.is_secure() else "http",
                    },
                )

                mail = EmailMessage(mail_subject, message, to=[email])

                if mail.send():
                    messages.info(
                        request, f"Check your {email} inbox to reset your password."
                    )
                else:
                    messages.info(request, f"We couldn't send an email to {email}.")

                return redirect("index")

            else:
                messages.warning(request, f"User {email} doesn't exist.")
                return redirect("reset_password_email")

    return render(request, "reset_password_email.html", context)


def set_new_password(request, uidb64, token):
    log_in_form = CustomUserLogInForm()
    form = CustomUserSetPasswordForm()

    context = {"log_in_form": log_in_form, 
               "form": form}

    if request.method == "POST":
        form = CustomUserSetPasswordForm(request.POST)

        if form.is_valid():
            uid = force_str(urlsafe_base64_decode(uidb64))

            try:
                user = CustomUser.objects.get(pk=uid)
            except:
                user = None

            if user is not None and default_token_generator.check_token(user, token):

                password = form.cleaned_data["password1"]

                if len(password) < 8:
                    messages.info(request, "Invalid password.")
                    return redirect("set_new_password", uidb64=uidb64, token=token)

                user.set_password(password)
                user.save()
                messages.info(request, "Password resetted. Now you can login.")
            else:
                messages.info(request, "Reset link is invalid!")

            return redirect("index")

    return render(request, "reset_password_password.html", context)


def log_out(request):
    global user
    logout(request)
    user = None
    messages.add_message(request, messages.INFO, "Now you're logged out.")
    return redirect("index")


def boxes(request):
    global user
    
    cities = pd.read_csv(settings.BASE_DIR / "static/all_cities.csv", sep=";", encoding="latin-1")
    print(cities)

    log_in_form = CustomUserLogInForm()
    filter_form = FilterForm()

    boxes = Box.objects.all()

    paginator = Paginator(boxes, 5)
    page = request.GET.get("page")
    boxes = paginator.get_page(page)

    if boxes.paginator.num_pages < 5:
        page_numbers = range(1, boxes.paginator.num_pages + 1)
    else:
        if boxes.number < 3:
            min = 1
        else:
            min = boxes.number - 2
        if boxes.number > boxes.paginator.num_pages - 2:
            max = boxes.paginator.num_pages + 1
        else:
            max = boxes.number + 3

        page_numbers = list(range(min, max))
        page_numbers.append("...")
        page_numbers.append(boxes.paginator.num_pages)

    log_in(request)
    
    if request.method == "POST":
        form = FilterForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data['city'])
        
    context = {
        "log_in_form": log_in_form,
        "filter_form": filter_form,
        "user": user,
        "boxes": boxes,
        "page_numbers": page_numbers,
    }

    return render(request, "boxes.html", context)


@login_required
def add_box(request):
    global user

    log_in_form = CustomUserLogInForm()
    form = AddBoxForm()

    if request.method == "POST":
        form = AddBoxForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.instance.user = user
                form.save()
                messages.add_message(request, messages.INFO, "Box added.")
                return redirect("boxes")
            except:
                messages.add_message(request, messages.INFO, "Something went wrong.")

    context = {"log_in_form": log_in_form, 
               "user": user, 
               "form": form}

    return render(request, "add_box.html", context)