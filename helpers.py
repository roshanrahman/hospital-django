from users.models import UserProfile
from hospital.models import Hospital
from specializations.models import Specialization
from appointment.models import Appointment
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
            'type': 'hospital'
        })
    for spec in specializations:
        results.append({
            'id': spec.id,
            'name': spec.name,
            'type': 'specialization'
        })
    return results


def get_hospital_json(hospital):
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
        doctors_json.append({
            'id': doctor.id,
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
            'specialization_name': doctor.specialization.name,
            'specialization_id': doctor.specialization.id,
        })
    hospital_json['doctors'] = doctors_json
    spec_json = []
    for specialization in hospital.specializations.all():
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
                hospitals_json.append(get_hospital_json(hospital))
            spec_json['hospitals'] = hospitals_json
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
    start_time = hospital.opening_hours
    end_time = hospital.closing_hours
    duration = hospital.session_duration
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    print(date_obj.isoformat())
    appointments = Appointment.objects.filter(
        appointment_status='pending',
        time_slot__date=date_obj, at_hospital=hospital_id, doctor=doctor_id)
    print(appointments)
    slots = build_time_slots(start_time, end_time, duration)
    for appointment in appointments:
        appointment.time_slot.replace(second=0)
        for slot in slots:
            if(is_time_between(
                appointment.time_slot.time(),
                (appointment.time_slot + datetime.timedelta(minutes=duration)).time(),
                slot['start']['full']
            )):
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
