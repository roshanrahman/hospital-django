from django.contrib import admin
from django.urls import path, include
from patient import views

app_name = 'patient'

urlpatterns = [
    path('', views.index, name="index"),
    path('new', views.new_appointment, name="new_appointment"),
    path('profile', views.patient_profile, name="profile")
]
