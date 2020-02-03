from django.urls import path, include
from app import views

app_name = 'app'
urlpatterns = [
    path('new', views.new_appointment, name='new_appointment'),
    path('', views.index, name='index'),
]
