from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from hospital_django.settings import EMAIL_HOST_USER
from hospital.models import Hospital
from appointment.models import Appointment
from specializations.models import Specialization
from users.models import UserProfile
from helpers import send_appointment_confirmation_email, search_results, get_data, build_time_slots, get_slots, get_today_appointments, get_upcoming_appointments
from datetime import datetime, timedelta


def delete_appointment_session(request):
    try:
        del request.session['booking']
    except Exception:
        pass


def redirect_if_no_session(request):
    try:
        a = request.session['booking']
        return False
    except Exception:
        return redirect('app:patient:index')


@login_required(login_url='/users/login')
def new_appointment(request):
    context = {
        'user': request.user
    }
    if(request.GET.get('search', None) is not None):
        query = request.GET.get('search')
        context['results'] = search_results(query)
        context['query'] = query

    return render(request, 'patient/new.html', context)


@login_required(login_url='/users/login')
def select_slot(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        hospital_id = request.POST.get('hospital_id')
        specialization_id = request.POST.get('specialization_id')

        if(not doctor_id or not hospital_id or not specialization_id):
            return JsonResponse({'error': 'Incorrect parameters'})
        request.session['booking'] = {
            'doctor_id': doctor_id,
            'hospital_id': hospital_id,
            'specialization_id': specialization_id
        }
        return redirect('app:patient:select_slot')
    if(redirect_if_no_session(request)):
        return (redirect_if_no_session(request))
    context = request.session['booking']
    return render(request, 'patient/slot.html', context)


@login_required(login_url='/users/login')
def payment(request):
    if(redirect_if_no_session(request)):
        return redirect_if_no_session(request)
    patient_id = request.user.id
    doctor_id = request.POST.get('doctor_id')
    hospital_id = request.POST.get('hospital_id')
    specialization_id = request.POST.get('specialization_id')
    date = request.POST.get('date')
    request.session['booking'] = {
        'doctor_id': doctor_id,
        'hospital_id': hospital_id,
        'specialization_id': specialization_id,
        'date': date
    }
    patient_data = UserProfile.objects.get(pk=int(patient_id))
    doctor_data = UserProfile.objects.get(pk=int(doctor_id))
    hospital_data = Hospital.objects.get(pk=int(hospital_id))
    specialization_data = Specialization.objects.get(pk=int(specialization_id))
    request.session['appointment'] = {
        'patient_name': f'{patient_data.first_name} {patient_data.last_name}',
        'doctor_name': f'Dr. {doctor_data.first_name} {doctor_data.last_name}',
        'hospital_name': f'{hospital_data.name}',
        'hospital_address': f'{hospital_data.address}',
        'specialization_name': f'{specialization_data.name}',
        'time_slot': f'{date}',
        'duration': hospital_data.session_duration
    }
    context = request.session['appointment']
    return render(request, 'patient/payment.html', context)


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


def get_data_json(request):
    return JsonResponse(get_data(request.GET.get('query'), request.GET.get('obj_type')), safe=False)


@login_required(login_url='/users/login')
def index(request):
    delete_appointment_session(request)
    try:
        del request.session['appointment']
    except Exception:
        pass
    today_appointments_list = get_today_appointments(request)
    upcoming_appointments_list = get_upcoming_appointments(request)
    context = {
        'today': today_appointments_list,
        'upcoming': upcoming_appointments_list
    }
    print(today_appointments_list)
    return render(request, 'patient/index.html', context)


def get_slots_json(request):
    hospital_id = request.GET.get('hospital_id')
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')
    if(not hospital_id or not doctor_id):
        return JsonResponse({
            'error': 'Missing parameters. Provide hospital_id and doctor_id'
        })
    slots = get_slots(hospital_id, doctor_id, date)
    return JsonResponse(slots, safe=False)


def make_appointment(request):
    if(redirect_if_no_session(request)):
        return redirect_if_no_session(request)
    patient_id = request.user.id
    doctor_id = request.session['booking']['doctor_id']
    hospital_id = request.session['booking']['hospital_id']
    specialization_id = request.session['booking']['specialization_id']
    date = request.session['booking']['date']
    appointment = Appointment.objects.create(
        with_specialization=Specialization.objects.get(
            pk=int(specialization_id)),
        doctor=UserProfile.objects.get(pk=int(doctor_id)),
        patient=UserProfile.objects.get(pk=int(patient_id)),
        at_hospital=Hospital.objects.get(pk=int(hospital_id)),
        time_slot=date,
        notes=''
    )
    with_specialization = Specialization.objects.get(
        pk=int(specialization_id))
    doctor = UserProfile.objects.get(pk=int(doctor_id))
    patient = UserProfile.objects.get(pk=int(patient_id))
    at_hospital = Hospital.objects.get(pk=int(hospital_id))
    print(doctor_id, hospital_id, specialization_id, date)
    send_appointment_confirmation_email(
        date,
        f'{patient.first_name} {patient.last_name}',
        patient.email,
        f'Dr. {doctor.first_name} {doctor.last_name}',
        with_specialization.name,
        at_hospital.name,
        at_hospital.address,
        at_hospital.contact
    )
    delete_appointment_session(request)
    return redirect('app:patient:success')


def success(request):
    context = request.session['appointment']
    return render(request, 'patient/success.html', context)
