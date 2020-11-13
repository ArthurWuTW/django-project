from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *
from django.db import connection

class PlantTableHandler(ModelDataHandler):
    def getData(self):
        # WARNING
        # You should be very careful whenever you write raw SQL.
        # Every time you use it, you should properly escape any parameters that
        # the user can control by using params in order to protect against SQL injection attacks.
        # Please read more about SQL injection protection.
        plant_table_title_list = list()
        plant_table_row_list = list()
        plant_table_title_list.append("")
        with connection.cursor() as cursor:
            cursor.execute("select distinct data_date from monitor_app_plantdata order by data_date")
            dates = cursor.fetchall()
            for date in dates:
                plant_table_title_list.append(date[0].strftime('%m/%d'))
            print(plant_table_title_list)

            cursor.execute("select distinct aruco_id from monitor_app_plantdata order by aruco_id")
            aruco_ids = cursor.fetchall()

            for aruco_id in aruco_ids:
                cursor.execute("select image_url from monitor_app_plantdata where aruco_id=%s order by data_date", [aruco_id[0]])
                image_urls = cursor.fetchall()
                image_urls = [url[0] for url in image_urls]
                image_urls.insert(0, str(aruco_id[0]))
                plant_table_row_list.append(image_urls)
        return json.dumps({
                    'title': plant_table_title_list,
                    'data': plant_table_row_list})
    def getTitle(self):
        return 'plant_table'
