from django.http import HttpResponse
from ..models import *

def updateWarningCount(request, status):
    task = TaskStatus.objects.get(task_name="WARNING COUNT")
    task.status = status
    task.save()

    return HttpResponse('succeed')
