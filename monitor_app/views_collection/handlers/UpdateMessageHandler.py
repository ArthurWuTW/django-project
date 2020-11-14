from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from .MessageCenterHandler import MessageCenterHandler
from ...models import *
from django.views.decorators.csrf import csrf_exempt

# Inherit MessageCenterHandler
class UpdateMessageHandler(MessageCenterHandler):
    def getData(self):
        unread_log_msg_num = int(self.request.POST.get('unread_num'))
        # Description: When call this view from ajax,
        # Filter out all unread messages and update to "read",
        # And render the code piece to respond ajax,
        # And then replace new html
        messagelog_data = list()
        now = datetime.now()
        messagelog_list = MessageLog.objects.filter(time__lte=now).order_by('-time')[:unread_log_msg_num+5]
        for log in messagelog_list:
            time_delta = now - log.time.replace(tzinfo=None)
            messagelog_data.append({
                'delta_time': self.convertTimeDeltaToDayHourMinString(time_delta),
                'title': log.title,
                'log': log.log,
                'type': log.type,
            })

        MessageLog.objects.filter(time__lte=now).update(read=True)
        # print(messagelog_data)
        return messagelog_data
