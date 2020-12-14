from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *

class WarningStatusHander(ModelDataHandler):
    def getData(self):
        #Status data
        warning_count = TaskStatus.objects.get(task_name="WARNING COUNT")
        return {
            'title': warning_count.task_name,
            'status': warning_count.status
        }
    def getTitle(self):
        return 'warning_count_data'

    def updateStatusData(self, statusData):
        task = TaskStatus.objects.get(task_name="WARNING COUNT")
        task.status = statusData
        task.save()

    def create_fake_data(self, status):
        task = TaskStatus()
        task.task_name = "WARNING COUNT"
        task.status = status
        task.save()
