from django.shortcuts import render
from django.urls import path, include
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return HttpResponse('The app works')


@login_required()
def secret_page(request):
    return HttpResponse('Secret contents!', status=200)


class MyProtectedEndPoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, there!!')
