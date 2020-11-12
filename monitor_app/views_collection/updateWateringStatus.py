from django.http import HttpResponse
from ..models import *

def updateWateringStatus(request, status):
    task = TaskStatus.objects.get(task_name="WATERING STATUS")
    task.status = status
    task.save()

    return HttpResponse('succeed')
