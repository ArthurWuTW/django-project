from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from datetime import datetime, timedelta

# Create your views here.
def dashboard(request):

    timezone_hour_offset = 8

    context = {
    }
    return render(request, 'template_dashboard/dashboard.html', context)

def temperature(request, temp):
    print("temp", temp)
    data = Temperature()
    data.temperature = temp
    data.time = datetime.now()
    print(data.temperature)
    print(data.time)
    data.save()

    return HttpResponse('')

def humidity(request, humid):
    print("humid", humid)
    data = Humidity()
    data.humidity = humid
    data.time = datetime.now()
    print(data.humidity)
    print(data.time)
    data.save()

    return HttpResponse('')
