from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *


class PiCpuTempStatusHander(ModelDataHandler):
    def getData(self):
        #Status data
        pi_cpu_temperature = TaskStatus.objects.get(task_name="PI CPU TEMPERATURE")
        return {
            'title': pi_cpu_temperature.task_name,
            'status': pi_cpu_temperature.status
        }
    def getTitle(self):
        return 'pi_cpu_temperature_data'

    def updateStatusData(self, statusData):
        task = TaskStatus.objects.get(task_name="PI CPU TEMPERATURE")
        task.status = statusData
        task.save()
