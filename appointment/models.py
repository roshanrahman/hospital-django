from django.db import models
from app.models import BaseModel
from specializations.models import Specialization
from users.models import UserProfile
from hospital.models import Hospital

APPOINTMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


# Create your models here.
class Appointment(BaseModel):
    with_specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE, related_name='+',
    )
    doctor = models.ForeignKey(UserProfile, limit_choices_to={
        'user_type': 'doctor'
    }, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(UserProfile, limit_choices_to={
        'user_type': 'patient'
    }, on_delete=models.CASCADE, related_name='patient')
    at_hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name='+')
    time_slot = models.DateTimeField()
    status = models.CharField(
        choices=APPOINTMENT_STATUS_CHOICES, max_length=20),
    notes = models.TextField(null=True)
