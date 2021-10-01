from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# form for the registration of a new user
class RegistrationForm(UserCreationForm):
    email = forms.CharField(max_length=50, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
