from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from helpers import redirect_to_correct_account, send_appointment_cancellation_email, send_appointment_confirmation_email, search_results, get_data, build_time_slots, get_slots, get_today_appointments, get_upcoming_appointments
from specializations.models import Specialization
from appointment.models import Appointment
from datetime import datetime, timedelta


@login_required(login_url='/')
def doctor_appointments(request):
    if redirect_to_correct_account(request, 'doctor'):
        return redirect('app:index')
    appointments = Appointment.objects.filter(doctor_id=request.user.id)
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
        {appointment.appointment_status}'''
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
    return render(request, 'doctor/appointments.html', context)


@login_required(login_url='/')
def doctor_profile(request):
    if redirect_to_correct_account(request, 'doctor'):
        return redirect('app:index')
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
        availability = [
            int(request.POST.get('monday', 1)),
            int(request.POST.get('tuesday', 1)),
            int(request.POST.get('wednesday', 1)),
            int(request.POST.get('thursday', 1)),
            int(request.POST.get('friday', 1)),
            int(request.POST.get('saturday', 1)),
            int(request.POST.get('sunday', 1)),
        ]
        user.weekday_availability = availability
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
    if redirect_to_correct_account(request, 'doctor'):
        return redirect('app:index')
    today_appointments_list = get_today_appointments(request, doctor=True)
    upcoming_appointments_list = get_upcoming_appointments(
        request, doctor=True)
    context = {
        'today': today_appointments_list,
        'upcoming': upcoming_appointments_list
    }
    return render(request, 'doctor/index.html', context)


@login_required(login_url='/')
def appointment_details(request, appointment_id=None):
    if redirect_to_correct_account(request, 'doctor'):
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
        except Exception:
            pass
        return redirect('app:doctor:doctor_appointments')
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
        return redirect('app:doctor:doctor_appointments')
    return render(request, 'doctor/appointment_detail.html', context)
