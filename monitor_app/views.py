from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from datetime import datetime, timedelta
from .view_utils import *
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def dashboard(request):

    time_threshold = datetime.now() - timedelta(hours=8)
    # gte : greater than equal
    temps = Temperature.objects.filter(time__gte=(time_threshold))
    humids = Humidity.objects.filter(time__gte=(time_threshold))

    timezone_hour_offset = 8

    temp_list = list()
    for temp in temps:
        temp_list.append({
            'timestamp': (temp.time + timedelta(hours=8)).strftime('%m/%d %H:%M'),
            'temperature': temp.temperature
        })

    print(temp_list)

    humid_list = list()
    for humid in humids:
        humid_list.append({
            'timestamp': (humid.time + timedelta(hours=8)).strftime('%m/%d %H:%M'),
            'humidity': humid.humidity
        })

    cpu_temp = CpuTemperature.objects.get(id=1)
    cpu_data = {
        'timestamp': cpu_temp.time,
        'temperature': cpu_temp.cpuTemperature
    }

    context = {
        'temp_list': temp_list,
        'humid_list': humid_list,
        'cpu_data': cpu_data
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
    data.save()

    return HttpResponse('')

def cpuTemperature(request, cpuTemp):
    print("cpu temp", cpuTemp)
    data = CpuTemperature.objects.get(id=1)
    data.cpuTemperature = cpuTemp
    data.time = datetime.now()
    data.save()

    return HttpResponse('')

@csrf_exempt
def receiveImage(request):

    if request.method == 'POST':

        received_data = json.loads(request.body.decode("utf-8"))

        raw_data = received_data['image']
        print("------------------------")
        # encoding decoding processing
        raw_data = raw_data.encode("utf-8")
        print(raw_data)

        import base64
        import numpy as np
        import cv2

        imgString = base64.b64decode(raw_data)
        np_array = np.fromstring(imgString, np.uint8)
        print(np_array)

        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        print(image)

        cv2.imwrite("./abc.jpg", image)


        return HttpResponse(str(received_data))

    return HttpResponse('Not post')
