from django.http import HttpResponse
from ..models import *
from datetime import datetime

def humidity(request, humid):
    print("humid", humid)
    data = Humidity()
    data.humidity = humid
    data.time = datetime.now()
    data.save()

    return HttpResponse('')
