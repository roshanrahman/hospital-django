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


import requests

CLIENT_ID = 'N76JH5EcYrkHMbx1Gzyl3VSwOE0o3MF3OaRvkxmw'
CLIENT_SECRET = 'n0ciCy2Ta3f7HpJ9YaqOyKCemsQox1yQiRV5OwAndOiEghLlRdTMeGQrNzRhTB9wBZ4hv5P20Sq980aHM5MpuKbNejkt2Cq2ZryvqLJr24dBVtzW0u5insFaiU1vKz80'


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
        except Exception as exp:
            messages.error(request, str(exp))
            return redirect('register')
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
            index_url = reverse('index')
            response = redirect(index_url)
            return response
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    if request.method == 'GET':
        return render(request, 'users/login.html')


def logout(request):
    auth_logout(request)
    messages.info("You've been logged out")
    return redirect(reverse('index'))
