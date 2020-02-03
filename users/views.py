from django.shortcuts import render, redirect
from django.urls import path, include, reverse
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login as auth_login, logout as auth_logout
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.forms import RegisterUserForm
from users.models import UserProfile
from oauth2_provider.models import AccessToken
from django.contrib import messages
from app.constants import CLIENT_ID, CLIENT_SECRET


import requests


def register(request):
    context = {
        'register_form': RegisterUserForm
    }
    if request.method == 'GET':
        return render(request, 'users/register.html', context=context)
    if request.method == 'POST':
        form_data = request.POST
        # TODO Validate
        try:
            user = UserProfile.objects.create_user(
                email=form_data.get('email'),
                password=form_data.get('password'),
                first_name=form_data.get('first_name'),
                last_name=form_data.get('last_name'),
                mobile=form_data.get('mobile'),
                user_type=form_data.get('user_type', 'patient')
            )
        except IntegrityError as err:
            messages.error(
                request, 'The email you provided already exists, please use another email')
            return redirect('users:register')
        except Exception as exp:
            messages.error(request, str(exp))
            return redirect('users:register')
        return render(request, 'users/success.html', context=context)


def login(request):
    if request.method == 'POST':
        r = requests.post('http://0.0.0.0:8000/o/token/',
                          data={
                              'grant_type': 'password',
                              'username': request.POST['email'],
                              'password': request.POST['password'],
                              'client_id': CLIENT_ID,
                              'client_secret': CLIENT_SECRET,
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
            messages.error(request, 'Invalid Credentials')
            return redirect('users:login')

    if request.method == 'GET':
        return render(request, 'users/login.html')


def logout(request):
    auth_logout(request)
    messages.info(request, "You've been logged out")
    return redirect(reverse('app:index'))


def approval_pending(request):
    if(request.user and not request.user.account_status == 'pending'):
        return redirect('app:index')
    return render(request, 'users/pending.html')


def account_blocked(request):
    if(request.user and not request.user.account_status == 'blocked'):
        return redirect('app:index')
    return render(request, 'users/blocked.html')
