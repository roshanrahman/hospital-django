from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from hospital.models import Hospital
from appointment.models import Appointment
from specializations.models import Specialization
from users.models import UserProfile
from helpers.email import send_appointment_cancellation_email, send_appointment_confirmation_email
from helpers.common import redirect_to_correct_account
from helpers.search import search_results, get_data
from helpers.appointments import get_slots, get_today_appointments, get_upcoming_appointments
from datetime import datetime, timedelta


def delete_appointment_session(request):
    try:
        del request.session['booking']
    except Exception:
        pass


def redirect_if_no_session(request):
    return False if request.session.get('booking', None) is not None else redirect('app:patient:index')


@login_required(login_url='/users/login')
def new_appointment(request):
    context = {
        'user': request.user
    }
    if redirect_to_correct_account(request, 'patient'):
        return redirect('app:index')
    if(request.GET.get('search', None) is not None):
        query = request.GET.get('search')
        context['results'] = search_results(query)
        context['query'] = query

    return render(request, 'patient/new.html', context)


@login_required(login_url='/users/login')
def select_slot(request):
    if redirect_to_correct_account(request, 'patient'):
        return redirect('app:index')
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
    if redirect_to_correct_account(request, 'patient'):
        return redirect('app:index')
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


@login_required(login_url='/')
def patient_appointments(request):
    if redirect_to_correct_account(request, 'patient'):
        return redirect('app:index')
    appointments = Appointment.objects.filter(patient_id=request.user.id)
    appointments_list = []
    search_query = request.GET.get('search')
    sort = request.GET.get('sort')
    if(sort == 'latest'):
        appointments = appointments.order_by('-time_slot')
    elif(sort == 'oldest'):
        appointments = appointments.order_by('time_slot')
    for appointment in appointments:
        slot_end = appointment.time_slot + \
            timedelta(minutes=appointment.at_hospital.session_duration)
        searchable_string = f'''{appointment.at_hospital.name}
        {appointment.patient.first_name}
        {appointment.patient.last_name}
        {appointment.doctor.first_name}
        {appointment.doctor.last_name}
        {appointment.appointment_status}
        '''
        if(search_query and search_query.lower() not in searchable_string.lower()):
            continue
        appointments_list.append({
            'id': appointment.id,
            'appointment_status': appointment.appointment_status,
            'with_specialization': appointment.with_specialization,
            'doctor': appointment.doctor,
            'patient': appointment.patient,
            'at_hospital': appointment.at_hospital,
            'time_slot': appointment.time_slot,
            'slot_start': datetime.strftime(appointment.time_slot, '%I:%M %p'),
            'slot_end': datetime.strftime(slot_end, '%I:%M %p'),
        })
    context = {
        'appointments': appointments_list
    }
    if(search_query):
        context['search'] = search_query
    if(sort):
        context['sort'] = sort
    return render(request, 'patient/appointments.html', context)


@login_required(login_url='/')
def patient_profile(request):
    if redirect_to_correct_account(request, 'patient'):
        return redirect('app:index')
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
    if redirect_to_correct_account(request, 'patient'):
        return redirect('app:index')
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


@login_required(login_url='/')
def make_appointment(request):
    if redirect_to_correct_account(request, 'patient'):
        return redirect('app:index')
    if(redirect_if_no_session(request)):
        return redirect_if_no_session(request)
    patient_id = request.user.id
    doctor_id = request.session['booking']['doctor_id']
    hospital_id = request.session['booking']['hospital_id']
    specialization_id = request.session['booking']['specialization_id']
    date = request.session['booking']['date']
    Appointment.objects.create(
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


@login_required(login_url='/')
def success(request):
    if redirect_to_correct_account(request, 'patient'):
        return redirect('app:index')
    context = request.session['appointment']
    return render(request, 'patient/success.html', context)


@login_required(login_url='/')
def appointment_details(request, appointment_id=None):
    if redirect_to_correct_account(request, 'patient'):
        return redirect('app:index')
    if request.method == 'POST':
        status = request.POST.get('status')
        reason = request.POST.get('reason', 'Reason not specified')
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.appointment_status = status
            appointment.notes = reason
            appointment.save()
            if(status == 'cancelled'):
                send_appointment_cancellation_email(
                    appointment.time_slot.strftime('%Y-%m-%d %H:%M'),
                    reason,
                    appointment.patient.first_name,
                    appointment.patient.email,
                    appointment.doctor.first_name,
                    appointment.with_specialization.name,
                    appointment.at_hospital.name,
                    appointment.at_hospital.address,
                    appointment.at_hospital.contact
                )
        except Exception as e:
            print(e)
        return redirect('app:patient:patient_appointments')
    context = dict()
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
        if appointment.time_slot.date() <= datetime.now().date():
            context['today'] = True
        if appointment.appointment_status == 'pending':
            context['allow_actions'] = True
        context['appointment'] = appointment

    except Exception as e:
        print(e)
        return redirect('app:patient:patient_appointments')
    return render(request, 'patient/appointment_detail.html', context)
