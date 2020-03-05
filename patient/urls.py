from django.contrib import admin
from django.urls import path, include
from patient import views

app_name = 'patient'

urlpatterns = [
    path('appointments', views.patient_appointments,
         name="patient_appointments"),
    path('appointments/<int:appointment_id>',
         views.appointment_details, name='appointment_detail'),
    path('new_appointment', views.new_appointment, name="new_appointment"),
    path('select_slot', views.select_slot, name="select_slot"),
    path('get_slots', views.get_slots_json, name='get_slots'),
    path('success', views.success, name='success'),
    path('payment', views.payment, name="payment"),
    path('profile', views.patient_profile, name="profile"),
    path('documents', views.patient_documents, name="documents"),
    path('documents/share', views.share_documents, name="share_document"),
    path('documents/add', views.patient_documents_add, name="add_document"),
    path('documents/<int:document_id>', views.patient_document_details,
         name="document_details"),
    path('search', views.search_results_json),
    path('get_data', views.get_data_json),
    path('get_doctor_emails', views.get_doctor_emails, name='get_doctor_emails'),
    path('make_appointment', views.make_appointment),
    path('', views.index, name="index"),
]
