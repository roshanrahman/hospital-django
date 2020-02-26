from users.models import UserProfile
from hospital.models import Hospital
from specializations.models import Specialization
from appointment.models import Appointment
from django.core.mail import send_mail
from django.template.loader import render_to_string
from hospital_django.settings import EMAIL_HOST_USER


import datetime


def search_results(query):
    doctors = UserProfile.objects.filter(
        first_name__icontains=query) | UserProfile.objects.filter(
            last_name__icontains=query)
    doctors = doctors.filter(
        user_type='doctor', account_status='active')
    hospitals = Hospital.objects.filter(
        name__icontains=query, status='active')
    specializations = Specialization.objects.filter(name__icontains=query)
    results = []
    for doctor in doctors:
        results.append({
            'id': doctor.id,
            'name': f'Dr. {doctor.first_name} {doctor.last_name}',
            'specialization': doctor.specialization.name if doctor.specialization is not None else 'not found',
            'type': 'doctor'
        })
    for hospital in hospitals:
        results.append({
            'id': hospital.id,
            'name': hospital.name,
            'address': hospital.address,
            'type': 'hospital'
        })
    for spec in specializations:
        results.append({
            'id': spec.id,
            'name': spec.name,
            'type': 'specialization'
        })
    return results


def get_hospital_json(hospital, only=None):
    hospital_json = {
        'hospital_id': hospital.id,
        'hospital_name': hospital.name,
        'session_duration': hospital.session_duration,
        'address': hospital.address,
        'opening_hours': hospital.opening_hours,
        'closing_hours': hospital.closing_hours,
        'contact': hospital.contact,
    }
    doctors_json = []
    for doctor in hospital.doctors.filter(account_status='active'):
        if(only is not None and not doctor.specialization.id == only):
            continue
        doctors_json.append({
            'id': doctor.id,
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
            'specialization_name': doctor.specialization.name if doctor.specialization else None,
            'specialization_id': doctor.specialization.id if doctor.specialization else None,
        })
    hospital_json['doctors'] = doctors_json
    spec_json = []
    for specialization in hospital.specialization.all():
        spec_json.append({
            'id': specialization.id,
            'name': specialization.name,
            'description': specialization.description
        })
    hospital_json['specializations'] = spec_json
    return hospital_json


def get_doctor_json(doctor):
    doctor_json = {
        'id': doctor.id,
        'first_name': doctor.first_name,
        'last_name': doctor.last_name,
        'specialization_name': doctor.specialization.name,
        'specialization_id': doctor.specialization.id,

    }
    hospitals = Hospital.objects.filter(doctors=doctor.id, status='active')
    hospitals_json = []
    for hospital in hospitals:
        hospitals_json.append({
            'hospital_id': hospital.id,
            'hospital_name': hospital.name,
            'session_duration': hospital.session_duration,
            'address': hospital.address,
            'opening_hours': hospital.opening_hours,
            'closing_hours': hospital.closing_hours,
            'contact': hospital.contact,
        })
    doctor_json['hospitals'] = hospitals_json
    return doctor_json


def get_data(query, obj_type):
    print('The query', query, obj_type)
    if(not query or not obj_type):
        return {
            'error': 'Please provide the parameters properly. query => the id of the object, obj_type => the type of object'
        }
    if(obj_type == 'doctor'):
        try:
            doctor = UserProfile.objects.get(pk=int(query))
            return get_doctor_json(doctor)

        except Exception as a:
            print(str(a))
            return {
                'error': f'No doctor found for id = {query} of type {obj_type}'
            }
    elif(obj_type == 'hospital'):
        try:
            hospital = Hospital.objects.get(pk=int(query))
            return get_hospital_json(hospital)
        except Exception as e:
            print(str(e))
            return {
                'error': f'No hospital found for id = {query} of type {obj_type}'
            }
    elif(obj_type == 'specialization'):
        try:
            specialization = Specialization.objects.get(pk=int(query))
            hospitals = Hospital.objects.filter(
                specialization=int(query), status='active')
            spec_json = {
                'id': specialization.id,
                'name': specialization.name,
                'description': specialization.description
            }
            hospitals_json = []
            for hospital in hospitals:
                hospitals_json.append(get_hospital_json(
                    hospital, only=specialization.id))
            spec_json['hospitals'] = hospitals_json
            print(spec_json)
            return spec_json
        except Exception as e:
            print(str(e))
            return {
                'error': f'No hospital found for id = {query} of type {obj_type}'
            }


def build_time_slots(start, end, duration):
    slots = []

    start = datetime.datetime(2020, 8, 1, start.hour,
                              start.minute, 0, 0)
    end = datetime.datetime(2020, 8, 1, end.hour,
                            end.minute, 0, 0)

    while((start + datetime.timedelta(minutes=duration)) < end):
        slot_start = start
        slot_end = start + datetime.timedelta(minutes=duration)
        slots.append(
            {
                'start': {
                    'full': slot_start.time(),
                    'hours':  slot_start.time().hour,
                    'minutes': slot_start.time().minute
                },
                'end': {
                    'full': slot_end.time(),
                    'hours':  slot_end.time().hour,
                    'minutes': slot_end.time().minute
                },
                'available': True
            }
        )
        start += datetime.timedelta(minutes=(duration + 1))
    return slots


def is_time_between(begin_time, end_time, check_time=None):
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def get_slots(hospital_id, doctor_id, date):
    hospital = Hospital.objects.get(
        pk=hospital_id)
    doctor = UserProfile.objects.get(pk=doctor_id)
    start_time = hospital.opening_hours
    end_time = hospital.closing_hours
    duration = hospital.session_duration
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    availability = doctor.weekday_availability
    day_of_week = date_obj.weekday()
    availability = availability[day_of_week]
    if(availability == 0):
        return {
            'working': False
        }
    appointments = Appointment.objects.filter(
        appointment_status='pending',
        time_slot__date=date_obj, at_hospital=hospital_id, doctor=doctor_id)
    print(appointments)
    slots = build_time_slots(start_time, end_time, duration)
    count = dict()
    for appointment in appointments:
        appointment.time_slot.replace(second=0)
        if(appointment.time_slot.strftime('%m/%d/%Y') not in count):
            count[appointment.time_slot.strftime('%m/%d/%Y')] = 1
        else:
            count[appointment.time_slot.strftime('%m/%d/%Y')] += 1
        for slot in slots:
            if(is_time_between(
                appointment.time_slot.time(),
                (appointment.time_slot + datetime.timedelta(minutes=duration)).time(),
                slot['start']['full']
            )):
                if(count[appointment.time_slot.strftime('%m/%d/%Y')] >= availability):
                    slot['available'] = False
    morning = []
    noon = []
    evening = []
    for slot in slots:
        if(slot['start']['hours'] >= 0 and slot['start']['hours'] < 12):
            morning.append(slot)
        if(slot['start']['hours'] >= 12 and slot['start']['hours'] < 16):
            noon.append(slot)
        if(slot['start']['hours'] >= 16):
            evening.append(slot)
    return {
        'morning': morning,
        'noon': noon,
        'evening': evening
    }


def get_today_appointments(request, doctor=None):
    today_appointments = Appointment.objects.filter(
        patient=request.user.id,
        time_slot__date=datetime.datetime.now().date(),
        appointment_status='pending'
    )
    if(doctor):
        today_appointments = Appointment.objects.filter(
            doctor=request.user.id,
            time_slot__date=datetime.datetime.now().date(),
            appointment_status='pending'
        )
    print(today_appointments)
    today_appointments_list = []
    for appointment in today_appointments:
        today_appointments_list.append({
            'id': appointment.id,
            'specialization_name': appointment.with_specialization.name,
            'appointment_status': appointment.appointment_status,
            'patient_name': f'{appointment.patient.first_name} {appointment.patient.last_name}',
            'hospital': {
                'name': appointment.at_hospital.name,
                'address': appointment.at_hospital.address,
                'contact': appointment.at_hospital.contact,
            },
            'doctor_name': f'Dr. {appointment.doctor.first_name} {appointment.doctor.last_name}',
            'timing': {
                'date': appointment.time_slot.date(),
                'date_string': datetime.datetime.strftime(appointment.time_slot, "%d %b %Y"),
                'time_slot': appointment.time_slot.time(),
                'time_slot_string': f'{ datetime.datetime.strftime(appointment.time_slot, "%I:%M %p")} to {   datetime.datetime.strftime(appointment.time_slot + datetime.timedelta(minutes=appointment.at_hospital.session_duration), "%I:%M %p")}'
            }
        })
    return today_appointments_list


def get_upcoming_appointments(request, doctor=None):
    upcoming_appointments = Appointment.objects.filter(
        patient=request.user.id,
        time_slot__date__gt=datetime.datetime.now().date(),
        appointment_status='pending'
    )
    if(doctor):
        upcoming_appointments = Appointment.objects.filter(
            doctor=request.user.id,
            time_slot__date__gt=datetime.datetime.now().date(),
            appointment_status='pending'
        )
    upcoming_appointments_list = []
    for appointment in upcoming_appointments:
        upcoming_appointments_list.append({
            'id': appointment.id,
            'specialization_name': appointment.with_specialization.name,
            'appointment_status': appointment.appointment_status,
            'patient_name': f'{appointment.patient.first_name} {appointment.patient.last_name}',
            'hospital': {
                'name': appointment.at_hospital.name,
                'address': appointment.at_hospital.address,
                'contact': appointment.at_hospital.contact,
            },
            'doctor_name': f'Dr. {appointment.doctor.first_name} {appointment.doctor.last_name}',
            'timing': {
                'date': appointment.time_slot.date(),
                'date_string': datetime.datetime.strftime(appointment.time_slot, "%d %b %Y"),
                'time_slot': appointment.time_slot.time(),
                'time_slot_string': f'{ datetime.datetime.strftime(appointment.time_slot, "%I:%M %p")} to {   datetime.datetime.strftime(appointment.time_slot + datetime.timedelta(minutes=appointment.at_hospital.session_duration), "%I:%M %p")}'
            }
        })
    return upcoming_appointments_list


def send_appointment_confirmation_email(date, patient_name, patient_email, doctor_name, specialization_name, hospital_name, hospital_address, hospital_contact):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
    context = {
        'date': datetime.datetime.strftime(date, '%A, %d %B %Y'),
        'time': datetime.datetime.strftime(date, '%I:%M %p'),
        'patient_name': patient_name,
        'doctor_name': doctor_name,
        'specialization_name': specialization_name,
        'hospital_name': hospital_name,
        'hospital_address': hospital_address,
        'hospital_contact': hospital_contact}

    msg_plain = render_to_string(
        'patient/email_success.txt', context)
    msg_html = render_to_string('patient/email_success.html',
                                context)
    if('noemail' in patient_email):
        patient_email = 'roshanrahman6399@gmail.com'
    send_mail(
        f'Appointment Booked for {datetime.datetime.strftime(date,"%d %b %Y")}',
        msg_plain,
        EMAIL_HOST_USER,
        [patient_email],
        html_message=msg_html
    )


def send_appointment_cancellation_email(date, reason, patient_name, patient_email, doctor_name, specialization_name, hospital_name, hospital_address, hospital_contact):
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
    context = {
        'date': datetime.datetime.strftime(date, '%A, %d %B %Y'),
        'time': datetime.datetime.strftime(date, '%I:%M %p'),
        'patient_name': patient_name,
        'doctor_name': doctor_name,
        'specialization_name': specialization_name,
        'hospital_name': hospital_name,
        'hospital_address': hospital_address,
        'hospital_contact': hospital_contact,
        'reason': reason
    }
    msg_plain = render_to_string(
        'patient/email_cancelled.txt', context)
    msg_html = render_to_string('patient/email_cancelled.html',
                                context)
    if('noemail' in patient_email):
        patient_email = 'roshanrahman6399@gmail.com'
    send_mail(
        f'Appointment Cancelled - {datetime.datetime.strftime(date,"%d %b %Y")}',
        msg_plain,
        EMAIL_HOST_USER,
        [patient_email],
        html_message=msg_html
    )


def redirect_to_correct_account(request, intended_account):
    try:
        if request.user.user_type == intended_account:
            return False
    except Exception:
        pass
    return True
