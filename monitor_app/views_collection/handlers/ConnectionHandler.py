from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *

class ConnectionHandler(ModelDataHandler):
    def __init__(self):
        self.timezone_shift = None
        self.threshold_timestamp = None
        self.server_name = None
        self.title = ""
    def setQueryServerName(self, server_name):
        self.server_name = server_name
    def setTimezoneShift(self, timedeltaObject):
        self.timezone_shift = timedeltaObject
        print(self.timezone_shift)
    def setThresholdTimestamp(self, datetimeObject):
        self.threshold_timestamp = datetimeObject
        print(self.threshold_timestamp)
    def getData(self): #override
        conns = Connections.objects.filter(time__gte=(self.threshold_timestamp), server_name=self.server_name)
        data = dict()
        data['timestamp_array'] = [(conn.time + self.timezone_shift).strftime('%m/%d %H:%M') for conn in conns]
        data['connections_array'] = [conn.number for conn in conns]
        return json.dumps(data)
    def setTitle(self, name):
        self.title = name
    def getTitle(self): #override
        return self.title
    def insertData(self, server_name, number):
        print("server_name", server_name)
        print("number", number)
        data = Connections()
        data.server_name = server_name
        data.number = number
        data.time = datetime.now()
        data.save()
        return 'succeed'
