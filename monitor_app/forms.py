from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from django import forms
from .models import *

class TemperatureForm(ModelForm):
    class Meta:
        model = Temperature
        exclude = ['temperature', 'time']
