from django.shortcuts import render
from django.urls import path, include
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.forms import RegisterUserForm
from users.models import UserProfile


def register(request):
    context = {
        'register_form': RegisterUserForm
    }
    if request.method == 'GET':
        return render(request, 'users/register.html', context=context)
    if request.method == 'POST':
        form_data = request.POST
        # TODO Validate
        new_user = UserProfile.objects.create_user(
            email=form_data.get('email'),
            password=form_data.get('password'),
            first_name=form_data.get('first_name'),
            last_name=form_data.get('last_name'),
            mobile=form_data.get('mobile'),
            user_type=form_data.get('user_type', 'patient')
        )
        messages.success(request, 'Successfully registered user')
        return render(request, 'users/register.html', context=context)
