from django.db import models
from app.models import BaseModel
from specializations.models import Specialization
from users.models import UserProfile
HOSPITAL_STATUS_CHOICES = [
    ('active', 'Active'),
    ('closed', 'Closed'),
]
# Create your models here.


class Hospital(BaseModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    session_duration = models.IntegerField(
        verbose_name='Treatment session (in minutes)')
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()
    status = models.CharField(
        max_length=255, default='active', choices=HOSPITAL_STATUS_CHOICES)
    specialization = models.ManyToManyField(Specialization)
    admin = models.ManyToManyField(UserProfile)
