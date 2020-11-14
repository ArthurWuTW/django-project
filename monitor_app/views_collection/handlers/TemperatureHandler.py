from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *

class TemperatureHandler(ModelDataHandler):
    def __init__(self):
        self.timezone_shift = None
        self.threshold_timestamp = None
    def setTimezoneShift(self, timedeltaObject):
        self.timezone_shift = timedeltaObject
        print(self.timezone_shift)
    def setThresholdTimestamp(self, datetimeObject):
        self.threshold_timestamp = datetimeObject
        print(self.threshold_timestamp)
    def getData(self): #override
        temps = Temperature.objects.filter(time__gte=(self.threshold_timestamp))
        data = dict()
        data['timestamp_array'] = [(temp.time + self.timezone_shift).strftime('%m/%d %H:%M') for temp in temps]
        data['temp_array'] = [temp.temperature for temp in temps]
        return json.dumps(data)
    def getTitle(self): #override
        return 'temp_data'
    def insertData(self, temp):
        print("temp", temp)
        data = Temperature()
        data.temperature = temp
        data.time = datetime.now()
        data.save()
        return 'succeed'
