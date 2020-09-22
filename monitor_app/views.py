from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from datetime import datetime, timedelta
from .view_utils import *
import json

# Create your views here.
def dashboard(request):

    temps = Temperature.objects.all()
    humids = Humidity.objects.all()

    timezone_hour_offset = 8

    temp_list = list()
    for temp in temps:
        temp_list.append({
            'timestamp': (temp.time + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'),
            'temperature': temp.temperature
        })

    print(temp_list)


    context = {
        'temp_list': temp_list
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
