from django.db import models
from app.models import BaseModel
from specializations.models import Specialization
from users.models import UserProfile

HOSPITAL_STATUS_CHOICES = [
    ('active', 'Active'),
    ('closed', 'Closed'),
]


class Hospital(BaseModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    session_duration = models.IntegerField(
        verbose_name='Treatment session (in minutes)')
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()
    specialization = models.ManyToManyField(Specialization, blank=True)
    doctors = models.ManyToManyField(UserProfile, limit_choices_to={
        'user_type': 'doctor'
    }, related_name='doctors', blank=True)
    status = models.CharField(
        max_length=255, default='active', choices=HOSPITAL_STATUS_CHOICES)
    admin = models.ManyToManyField(
        UserProfile, related_name='admins', blank=True)
    working_on_weekend = models.BooleanField(default=False)
    other_holidays = models.TextField(null=True, blank=True)


class Holidays(BaseModel):
    date = models.DateField()
    name = models.CharField(max_length=200)
