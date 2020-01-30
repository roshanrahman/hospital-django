from django.db import models
from users.models import UserProfile

APPOINTMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('complete', 'Complete'),
    ('cancelled', 'Cancelled'),
]


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    session_duration = models.IntegerField(
        verbose_name='Treatment session (in minutes)')
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()


class DoctorsInHospital(models.Model):
    doctor = models.ForeignKey(UserProfile, limit_choices_to={
                               'user_type': 'doctor'}, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)


class Specialization(models.Model):
    name = models.CharField(max_length=100)


class Appointment(models.Model):
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE)
    doctor = models.ForeignKey(UserProfile, limit_choices_to={
        'user_type': 'doctor'
    }, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(UserProfile, limit_choices_to={
        'user_type': 'patient'
    }, on_delete=models.CASCADE, related_name='patient')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    time = models.DateField()
    status = models.CharField(
        choices=APPOINTMENT_STATUS_CHOICES, max_length=20),
    notes = models.TextField(null=True)


class DoctorSpecialization(models.Model):
    doctor = models.ForeignKey(UserProfile, limit_choices_to={
        'user_type': 'doctor'
    }, on_delete=models.CASCADE)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE)


class HospitalSpecialization(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE)


class HospitalAdmin(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
