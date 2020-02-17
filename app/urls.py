from django.urls import path, include
from app import views as app_views
from hospitaladmin import views as hospitaladmin_views

app_name = 'app'

urlpatterns = [
    path('view-users', hospitaladmin_views.view_users),
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('social/', include('social_django.urls', namespace='social')),
    path('', app_views.index, name='index'),
]
