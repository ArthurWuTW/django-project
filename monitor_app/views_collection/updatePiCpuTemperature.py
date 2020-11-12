from django.http import HttpResponse
from ..models import *

def updatePiCpuTemperature(request, status):
    task = TaskStatus.objects.get(task_name="PI CPU TEMPERATURE")
    task.status = status
    task.save()

    return HttpResponse('succeed')
