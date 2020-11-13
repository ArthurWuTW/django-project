from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *

class HumidityHandler(ModelDataHandler):
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
        humids = Humidity.objects.filter(time__gte=(self.threshold_timestamp))
        data = dict()
        data['timestamp_array'] = [(humid.time + timedelta(hours=8)).strftime('%m/%d %H:%M') for humid in humids]
        data['humid_array'] = [humid.humidity for humid in humids]
        return json.dumps(data)
    def getTitle(self): #override
        return 'humid_data'
