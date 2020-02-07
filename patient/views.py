from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from helpers import search_results


def new_appointment(request):
    context = {
        'user': request.user
    }
    if(request.GET.get('search', None) is not None):
        query = request.GET.get('search')
        context['results'] = search_results(query)
        context['query'] = query

    return render(request, 'patient/new.html', context)


def patient_appointments(request):
    return render(request, 'patient/appointments.html')


def patient_profile(request):
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
    return render(request, 'patient/profile.html', context)


def search_results_json(request):
    query = request.GET.get('query', '')
    return JsonResponse(search_results(query), safe=False)


def index(request):
    return render(request, 'patient/index.html')
