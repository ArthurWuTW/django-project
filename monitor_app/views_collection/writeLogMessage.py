from django.http import HttpResponse
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from datetime import datetime, timedelta

def countWarningMessage():
    task = TaskStatus.objects.get(task_name="WARNING COUNT")
    task.status = str(int(task.status)+1)
    task.save()

def writeLogMessage(request, title, msg, type):
    group = AuthGroup.objects.get(group="Author")
    profiles = Profile.objects.filter(permission=group)
    print(group)
    print(profiles)
    now = datetime.now()
    for profile in profiles:
        message = MessageLog()
        message.user = profile.user
        message.time = now
        message.title = title
        message.log = msg
        message.read = False
        message.type = type
        message.save()

    # update warning count
    if(type=="WARNING"):
        countWarningMessage()

    return HttpResponse('succeed')
