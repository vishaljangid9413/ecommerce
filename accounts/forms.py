from .models import *
from django import forms

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile', 'password')



