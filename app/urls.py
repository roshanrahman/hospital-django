from django.urls import path, include
from app import views as app_views
from hospitaladmin import views as hospitaladmin_views

app_name = 'app'

urlpatterns = [
    path('view-users', hospitaladmin_views.view_users),
    path('patient/', include('patient.urls', namespace='home')),
    path('', app_views.index, name='index'),
]
