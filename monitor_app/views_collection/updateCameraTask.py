from django.http import HttpResponse
from ..models import *

def updateCameraTask(request, status):
    task = TaskStatus.objects.get(task_name="CAMERA TASK")
    task.status = status
    task.save()

    return HttpResponse('succeed')
