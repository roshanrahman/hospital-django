from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def doctor_appointments(request):
    return render(request, 'doctor/appointments.html')


def doctor_profile(request):
    if(request.method == 'POST'):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.mobile = mobile
        user.save()
        messages.success(request, 'Profile details have been updated')
    context = {
        'user': request.user
    }
    return render(request, 'doctor/profile.html', context)


@login_required(login_url='/users/login')
def index(request):

    return render(request, 'doctor/index.html')
