from django.http import HttpResponse
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from datetime import datetime, timedelta

def writeLogMessage(request, title, msg):
    group = AuthGroup.objects.get(group="Author")
    profiles = Profile.objects.filter(permission=group)
    print(group)
    print(profiles)
    for profile in profiles:
        message = MessageLog()
        message.user = profile.user
        message.time = datetime.now()
        message.title = title
        message.log = msg
        message.read = False
        message.save()

    return HttpResponse('succeed')
