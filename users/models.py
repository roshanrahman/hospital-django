from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserProfileManager

USER_TYPE_CHOICES = [
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
]


class UserProfile(AbstractUser):
    username = None
    email = models.EmailField('Email Address', unique=True)
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    mobile = models.CharField('Mobile Number', max_length=13)
    user_type = models.CharField(
        'User type', max_length=10,  choices=USER_TYPE_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserProfileManager()

    def __str__(self):
        return f'{self.email} ({self.user_type})'
