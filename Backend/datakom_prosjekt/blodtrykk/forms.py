from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Patient


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + \
            ("email", "first_name", "last_name")


class AccessToRegistrationForm(forms.Form):
    access_code = forms.CharField(
        max_length=32, required=True, label="Access code")


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'birthDate', 'phone', 'address')
