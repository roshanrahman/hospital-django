from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserProfileManager
from safedelete.models import SafeDeleteModel
from specializations.models import Specialization
# from softdelete.models import SOFT_DELETE_CASCADE


USER_TYPE_CHOICES = [
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
    ('admin', 'Admin')
]

ACCOUNT_STATUS_CHOICES = [
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked')
]


class UserProfile(AbstractUser, SafeDeleteModel):
    # _safedelete_policy = SOFT_DELETE_CASCADE
    username = None
    email = models.EmailField('Email Address', unique=True)
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField(
        'Last Name', max_length=50, null=True, default='')
    mobile = models.CharField('Mobile Number', max_length=13)
    user_type = models.CharField(
        'User type', max_length=10,  choices=USER_TYPE_CHOICES)
    account_status = models.CharField(
        choices=ACCOUNT_STATUS_CHOICES, max_length=20, default='pending')
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE, null=True,)
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(
        max_length=255, blank=True, null=True, default=None)
    working_on_weekend = models.BooleanField(default=False)
    working_on_holidays = models.BooleanField(default=False)
    other_holidays = models.TextField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserProfileManager()

    def __str__(self):
        return f'UserProfile({self.id}) {self.email} ({self.user_type})'
