from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *


class WateringStatusHander(ModelDataHandler):
    def getData(self):
        #Status data
        watering_status = TaskStatus.objects.get(task_name="WATERING STATUS")
        return {
            'title': watering_status.task_name,
            'status': watering_status.status
        }
    def getTitle(self):
        return 'watering_status_data'
