from django import forms
from users.models import USER_TYPE_CHOICES


class RegisterUserForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=50)
    last_name = forms.CharField(label="Last Name", max_length=50)
    email = forms.EmailField(label="Email Address", max_length=50)
    mobile = forms.CharField(label="Mobile Number", max_length=12)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
