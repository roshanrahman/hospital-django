from django.shortcuts import render

# Create your views here.


def view_users(request):
    return render(request, 'hospital-admin/users.html')
