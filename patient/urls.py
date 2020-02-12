from django.contrib import admin
from django.urls import path, include
from patient import views

app_name = 'patient'

urlpatterns = [
    path('appointments', views.patient_appointments,
         name="patient_appointments"),
    path('new_appointment', views.new_appointment, name="new_appointment"),
    path('select_slot', views.select_slot, name="select_slot"),
    path('get_slots', views.get_slots_json, name='get_slots'),
    path('payment', views.payment, name="payment"),
    path('profile', views.patient_profile, name="profile"),
    path('search', views.search_results_json),
    path('get_data', views.get_data_json),
    path('', views.index, name="index"),
]
