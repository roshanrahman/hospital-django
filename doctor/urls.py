from django.contrib import admin
from django.urls import path, include
from doctor import views

app_name = 'doctor'

urlpatterns = [
    path('appointments', views.doctor_appointments,
         name="doctor_appointments"),
    path('profile', views.doctor_profile, name="profile"),
    path('', views.index, name="index"),
]
