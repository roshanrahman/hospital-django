from django.urls import path, include
from app import views
urlpatterns = [
    path('', views.MyProtectedEndPoint.as_view()),
    path('secret', views.secret_page, name='secret'),
]
