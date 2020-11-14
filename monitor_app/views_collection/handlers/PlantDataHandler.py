from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *


class PlantDataHandler(ModelDataHandler):
    def getData(self): # override
        # WARNING
        # You should be very careful whenever you write raw SQL.
        # Every time you use it, you should properly escape any parameters that
        # the user can control by using params in order to protect against SQL injection attacks.
        # Please read more about SQL injection protection.
        sql_command = '\
        SELECT * FROM monitor_app_plantdata \
        WHERE data_date IN (SELECT max(data_date) FROM monitor_app_plantdata) \
        ORDER BY aruco_id ASC; \
        '
        plant_array = list()
        for plant in PlantData.objects.raw(sql_command):
            plant_array.append({
                'Id': plant.aruco_id,
                'Image': plant.image_url,
                'Type': plant.type,
                'Data Date': plant.data_date.strftime('%m/%d'),
                'Seed Date': plant.seed_date.strftime('%m/%d'),
                'Status': plant.status,
                'Growth_rate': plant.growth_rate
            })
        data = dict()
        data['plants'] = plant_array
        return json.dumps(data)
    def getTitle(self):
        return 'plants_data'
