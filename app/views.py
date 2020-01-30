from django.shortcuts import render
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
    return render(request, 'app/index.html', context)
