from django.contrib import admin
from django.urls import path, include
from patient import views

app_name = 'patient'

urlpatterns = [
    path('appointments', views.patient_appointments,
         name="patient_appointments"),
    path('new_appointment', views.new_appointment, name="new_appointment"),
    path('profile', views.patient_profile, name="profile"),
    path('search', views.search_results_json),
    path('', views.index, name="index"),
]
