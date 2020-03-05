from django.db import models
from app.models import BaseModel
from users.models import UserProfile
from patient.models import Document
from appointment.models import Appointment
# Create your models here.


class SharedDocument(BaseModel):
    doctor = models.ForeignKey(to=UserProfile, limit_choices_to={
        'user_type': 'doctor'
    }, on_delete=models.CASCADE)
    shared_document = models.ForeignKey(
        to=Document, on_delete=models.CASCADE, related_name='shareddoc')
    password = models.CharField(max_length=30)


class Feedback(models.Model):
    """Model definition for Feedback."""
    rating = models.IntegerField()
    doctor = models.ForeignKey(to=UserProfile, limit_choices_to={
        'user_type': 'doctor'
    }, on_delete=models.CASCADE, related_name='doctor_feedback')
    patient = models.ForeignKey(to=UserProfile, limit_choices_to={
        'user_type': 'patient'
    }, on_delete=models.CASCADE, related_name='patient_feedback')
    appointment = models.ForeignKey(to=Appointment, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        """Meta definition for Feedback."""

        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        """Unicode representation of Feedback."""
        return f'{self.id} - Doctor={self.doctor.first_name} Patient={self.patient.first_name} Rating={self.rating}'
