from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *

class CameraTaskStatusHander(ModelDataHandler):
    def getData(self):
        #Status data
        camera_task = TaskStatus.objects.get(task_name="CAMERA TASK")
        return {
            'title': camera_task.task_name,
            'status': camera_task.status
        }
    def getTitle(self):
        return 'camera_task_data'

    def updateStatusData(self, statusData):
        task = TaskStatus.objects.get(task_name="CAMERA TASK")
        task.status = statusData
        task.save()
