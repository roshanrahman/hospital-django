from django.shortcuts import render, redirect
from django.urls import path, include, reverse
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.decorators import protected_resource
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

# Create your views here.
@login_required(login_url='users/login')
def index(request):
    context = {
        'user': request.user
    }
    if not (request.user or request.user.is_authenticated()):
        return redirect('users:login')
    if(request.user.account_status == 'pending'):
        return redirect('users:approval_pending')
    elif(request.user.account_status == 'blocked'):
        return redirect('users:account_blocked')
    if(request.user.user_type == 'patient'):
        return render(request, 'patient/index.html', context)
    elif(request.user.user_type == 'doctor'):
        return render(request, 'doctor/index.html', context)
    elif(request.user.user_type == 'admin'):
        return render(request, 'hospital-admin/index.html', context)
