from users.models import UserProfile
from hospital.models import Hospital
from specializations.models import Specialization
from appointment.models import Appointment
from django.core.mail import send_mail
from django.template.loader import render_to_string
from hospital_django.settings import EMAIL_HOST_USER


import datetime


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


def send_appointment_cancellation_email(date, reason, patient_name, patient_email, doctor_name, specialization_name, hospital_name, hospital_address,
                                        hospital_contact):
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
