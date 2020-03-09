from django.db import models
from app.models import BaseModel
from users.models import UserProfile
# Create your models here.


class Document(BaseModel):
    """Model definition for Document."""
    title = models.CharField(max_length=200)
    url = models.TextField()
    patient = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, limit_choices_to={
        'user_type': 'patient'
    })
