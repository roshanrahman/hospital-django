from users.models import UserProfile
from hospital.models import Hospital
from appointment.models import Appointment
import datetime
from django.utils import timezone


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
    return check_time >= begin_time or check_time <= end_time


def is_time_after(end_time=None, check_time=None):
    return end_time > check_time


def is_ongoing(appointment_date, duration):
    now_date = timezone.now() + datetime.timedelta(hours=5, minutes=30)
    end_date = appointment_date + datetime.timedelta(minutes=duration)
    is_between = is_time_between(
        appointment_date.time(), end_date.time(), now_date.time()
    )
    is_after = end_date.time() < now_date.time()
    print('Returned by is_ongoing', is_between, is_after)
    if is_between:
        return {
            'is_ongoing': True,
            'status': 'in-progress',
            'long': 'Appointment is in progress'
        }
    if is_after:
        return {
            'is_ongoing': False,
            'status': 'time-elapsed',
            'long': 'The time for the appointment has elapsed, status not updated'
        }
    return False


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
        ongoing = is_ongoing(appointment.time_slot,
                             appointment.at_hospital.session_duration)
        print(ongoing)
        today_appointments_list.append({
            'id': appointment.id,
            'ongoing': ongoing,
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
        ongoing = False
        if appointment.appointment_status == 'pending':
            if timezone.now() > appointment.time_slot:
                ongoing = True
        upcoming_appointments_list.append({
            'id': appointment.id,
            'ongoing': ongoing,
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
