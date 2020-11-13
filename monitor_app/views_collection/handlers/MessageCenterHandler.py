from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *

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
