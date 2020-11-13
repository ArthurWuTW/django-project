from django.shortcuts import render
from ..models import *
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User

import abc
class ModelDataHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getData(self):
        return NotImplemented
    @abc.abstractmethod
    def getTitle(self):
        return NotImplemented

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

class MessageCenterHandler(ModelDataHandler):
    def __init__(self, request):
        self.request = request
        self.now = None
    def setNow(self,datetimeObject):
        self.now = datetimeObject
    def convertTimeDeltaToDayHourMinString(self,delta_time):
        day_str = str(delta_time.days)+"d " if delta_time.days is not 0 else ""
        hour_str = str(delta_time.seconds//3600)+"h " if delta_time.seconds//3600 is not 0 else ""
        min_str = str((delta_time.seconds//60)%60)+"m " if (delta_time.seconds//60)%60 is not 0 else ""
        is_just_now = True if delta_time.days is 0 and (delta_time.seconds//60)%60 is 0 else False
        return_str = ""
        if(is_just_now):
            return "In a minute"
        else:
            return day_str+hour_str+min_str+"ago"
    def getData(self):
        # Message center
        message = list()
        unread_log_msg_num = 0
        if(self.request.user.is_authenticated):
            current_user = User.objects.get(username = self.request.user.username)
            # print(current_user)
            profile = Profile.objects.get(user = current_user)
            # print(profile.activated)
            if(profile.activated):
                unread_log_msg_num = len(MessageLog.objects.filter(user = current_user, read=False))
                log_msg = MessageLog.objects.filter(user = current_user).order_by('-time')[:unread_log_msg_num+5]
                # print(log_msg)
                for log in log_msg:
                    time_delta = self.now - log.time.replace(tzinfo=None)
                    # print(log.time)
                    message.append({
                        'delta_time': self.convertTimeDeltaToDayHourMinString(time_delta),
                        'title': log.title,
                        'type': log.type,
                        'log': log.log,
                        'read': log.read
                    })
        messagelog_data = dict()
        # print("unread_log_msg_num", unread_log_msg_num)
        messagelog_data['unread_red_message_number'] = unread_log_msg_num
        messagelog_data['messagelog_array'] = message
        return json.dumps(messagelog_data)
    def getTitle(self):
        return 'messagelog_data'

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


class ContextHandler():
    def __init__(self):
        self.data_handler_list = list()
        self.context = {}
    def join(self, dataHandler):
        self.data_handler_list.append(dataHandler)
    def fillInContext(self):
        for data in self.data_handler_list:
            self.context[data.getTitle()] = data.getData()
    def clearContext(self):
        self.context = {}
    def getContext(self):
        return self.context



def dashboard(request):

    now = datetime.now()
    threshold_timestamp = now - timedelta(hours=8)

    tempHandler = TemperatureHandler()
    tempHandler.setTimezoneShift(timedelta(hours=8))
    tempHandler.setThresholdTimestamp(threshold_timestamp)

    humidHandler = HumidityHandler()
    humidHandler.setTimezoneShift(timedelta(hours=8))
    humidHandler.setThresholdTimestamp(threshold_timestamp)

    planthandler = PlantDataHandler()

    messageHandler = MessageCenterHandler(request)
    messageHandler.setNow(now)

    piCpuTempHander = PiCpuTempStatusHander()
    wateringStatusHandler = WateringStatusHander()
    cameraSatausHander = CameraTaskStatusHander()
    warningStatusHandler = WarningStatusHander()

    contextHandler = ContextHandler()
    contextHandler.join(tempHandler)
    contextHandler.join(humidHandler)
    contextHandler.join(planthandler)
    contextHandler.join(messageHandler)
    contextHandler.join(piCpuTempHander)
    contextHandler.join(wateringStatusHandler)
    contextHandler.join(cameraSatausHander)
    contextHandler.join(warningStatusHandler)
    contextHandler.fillInContext()

    return render(request, 'template_dashboard/dashboard.html', contextHandler.getContext())
