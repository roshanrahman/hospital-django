from django.shortcuts import render, redirect
from django.urls import path, include, reverse
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login, logout as auth_logout
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.forms import RegisterUserForm
from users.models import UserProfile
from specializations.models import Specialization
from oauth2_provider.models import AccessToken
from django.contrib import messages
from hospital_django.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
from hospital_django.settings import EMAIL_HOST_USER, BASE_URL
import secrets
import requests
from urllib.parse import urlencode


def register(request):
    context = {
        'register_form': RegisterUserForm,
        'specializations': Specialization.objects.all()
    }
    if request.method == 'GET':
        return render(request, 'users/register.html', context=context)
    if request.method == 'POST':
        form_data = request.POST
        print(form_data)
        # TODO Validate
        try:
            specialization = form_data.get('specialization')
            if(form_data.get('user_type') == 'patient'):
                specialization = None
            user = UserProfile.objects.create_user(
                email=form_data.get('email'),
                password=form_data.get('password'),
                first_name=form_data.get('first_name'),
                last_name=form_data.get('last_name'),
                mobile=form_data.get('mobile'),
                user_type=form_data.get('user_type', 'patient'),
                account_status="pending",
                specialization_id=int(
                    specialization) if specialization else None
            )
        except IntegrityError as err:
            print(err)
            messages.error(
                request, 'The email you provided already exists, please use another email address')
            return redirect('users:register')
        except Exception as exp:
            messages.error(request, str(exp))
            return redirect('users:register')
        auth_login(request, user,
                   backend='oauth2_provider.backends.OAuth2Backend')
        return render(request, 'users/success.html')


def fill_missing(request):
    context = {
        'user': request.user,
        'specializations': Specialization.objects.all()
    }
    if request.method == 'GET':
        return render(request, 'users/fill_missing.html', context=context)
    if request.method == 'POST':
        form_data = request.POST
        # TODO Validate
        print(form_data)
        print(form_data.get('mobile'))
        print(form_data.get('user_type'))
        try:
            user = UserProfile.objects.get(email=request.user.email)
            user.first_name = form_data.get('first_name')
            user.last_name = form_data.get('last_name')
            user.mobile = form_data.get('mobile')
            user.user_type = form_data.get('user_type')
            user.account_status = "active"
            user.save()
        except IntegrityError as err:
            print(err)
            messages.error(
                request, 'There was an error trying to register your account')
            return redirect('users:fill_missing')
        except Exception as exp:
            print(exp)
            messages.error(request, str(exp))
            return redirect('users:fill_missing')
        auth_login(request, user,
                   backend='oauth2_provider.backends.OAuth2Backend')
        return redirect('app:index')


def on_external_oauth(request):
    user = request.user
    if(not user.user_type or not user.mobile or not user.first_name):
        return redirect('users:fill_missing')
    return redirect('app:index')


def login(request):
    if request.method == 'POST':
        user = UserProfile.objects.filter(email=request.POST['email'])
        if(not user.exists()):
            messages.error(
                request, 'No account exists with the email address you provided')
            return redirect('users:login')
        r = requests.post(f'{BASE_URL}/token/',
                          data={
                              'grant_type': 'password',
                              'username': request.POST['email'],
                              'password': request.POST['password'],
                              'client_id': OAUTH_CLIENT_ID,
                              'client_secret': OAUTH_CLIENT_SECRET,
                          },
                          )
        if(r.json().get('access_token', None)) is not None:
            token = r.json().get('access_token')
            user_token = AccessToken.objects.get(
                token=token)
            user = user_token.user
            auth_login(request, user,
                       backend='oauth2_provider.backends.OAuth2Backend')
            index_url = reverse('app:index')
            response = redirect(index_url)
            return response
        else:
            print(r.json())
            messages.error(request, 'Invalid Credentials')
            return redirect('users:login')

    if request.method == 'GET':
        return render(request, 'users/login.html')


def logout(request):
    auth_logout(request)
    messages.info(request, "You've been logged out")
    return redirect(reverse('app:index'))


def approval_pending(request):
    if(request.user.is_authenticated and not request.user.account_status == 'pending'):
        return redirect('app:index')
    context = {
        'user': request.user
    }
    if(not request.user.is_authenticated):
        return redirect('app:index')
    return render(request, 'users/pending.html', context)


def account_blocked(request):
    if(request.user and not request.user.account_status == 'blocked'):
        return redirect('app:index')
    return render(request, 'users/blocked.html')


def send_email(request):
    if(not request.user.is_authenticated):
        return redirect('users:approval_pending')
    email_to = request.user.email
    if('noemail' in email_to):
        email_to = 'roshanrahman6399@gmail.com'
    user_id = request.user.id
    verification_token = secrets.token_hex(16)
    url = f'{BASE_URL}/users/verify_email'
    params = urlencode({
        'user_id': user_id,
        'code': verification_token
    })
    url = f'{url}?{params}'
    send_mail(
        'Verification link for Hospital Django',
        f'The verification link to verify your account on Hospital Django is {url}',
        EMAIL_HOST_USER,
        [email_to],
        fail_silently=False,
    )
    print('The verification url is ', url)
    user = UserProfile.objects.get(pk=user_id)
    # user.email_verified = False
    # user.account_status = 'pending'
    user.email_verification_code = verification_token
    user.save()
    messages.info(request,
                  'Verification link sent to your email address. Please check your inbox.')
    return redirect('users:approval_pending')


def verify_email(request):
    # user_id = request.GET.get('user_id', None)
    verification_token = request.GET.get('code', None)
    try:
        if verification_token:
            user = UserProfile.objects.get(
                email_verification_code=verification_token)
            # if(user.email_verification_code == verification_token):
            user.email_verified = True
            user.account_status = 'active'
            user.email_verification_code = None
            user.save()
            messages.success(
                request, 'Your email has been verified. You can now login.')
            return redirect('users:login')
        else:
            messages.error(request, "The verification link has expired")
    except Exception:
        messages.error(request, 'The verification link is invalid')
    return redirect('users:approval_pending')
