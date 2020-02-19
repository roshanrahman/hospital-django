from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from specializations.models import Specialization


def doctor_appointments(request):
    return render(request, 'doctor/appointments.html')


def doctor_profile(request):
    if(request.method == 'POST'):
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        working_on_weekend = request.POST.get('working_on_weekend')
        if(working_on_weekend == 'on'):
            working_on_weekend = True
        else:
            working_on_weekend = False
        working_on_holidays = request.POST.get('working_on_holidays')
        if working_on_holidays == 'on':
            working_on_holidays = True
        else:
            working_on_holidays = False
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.mobile = mobile
        user.working_on_weekend = working_on_weekend
        user.working_on_holidays = working_on_holidays
        user.save()
        messages.success(request, 'Profile details have been updated')
    specializations = Specialization.objects.all()
    context = {
        'user': request.user,
        'specializations': specializations
    }
    return render(request, 'doctor/profile.html', context)


@login_required(login_url='/users/login')
def index(request):

    return render(request, 'doctor/index.html')
