from django.contrib import admin
from django.urls import path, include
from doctor import views

app_name = 'doctor'

urlpatterns = [
    path('appointments', views.doctor_appointments,
         name="doctor_appointments"),
    path('appointments/<int:appointment_id>',
         views.appointment_details, name='appointment_detail'),
    path('profile', views.doctor_profile, name="profile"),
    path('documents', views.doctor_documents, name='doctor_documents'),
    path('documents/view', views.open_document, name='open_document'),
    path('', views.index, name="index"),
]
