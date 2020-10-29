from django.http import HttpResponse
from ..models import *
from datetime import datetime

def cpuTemperature(request, cpuTemp):
    print("cpu temp", cpuTemp)
    data = CpuTemperature.objects.get(id=1)
    data.cpuTemperature = cpuTemp
    data.time = datetime.now()
    data.save()

    return HttpResponse('')
