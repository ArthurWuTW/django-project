from django.shortcuts import render
from ..models import *
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta

def convertTimeDeltaToDayHourMinString(delta_time):

    day_str = str(delta_time.days)+"d " if delta_time.days is not 0 else ""
    hour_str = str(delta_time.seconds//3600)+"h " if delta_time.seconds//3600 is not 0 else ""
    min_str = str((delta_time.seconds//60)%60)+"m " if (delta_time.seconds//60)%60 is not 0 else ""
    is_just_now = True if delta_time.days is 0 and (delta_time.seconds//60)%60 is 0 else False

    return_str = ""
    if(is_just_now):
        return "In a minute"
    else:
        return day_str+hour_str+min_str+"ago"

@csrf_exempt
def updateLogMessage(request):
    unread_log_msg_num = int(request.POST.get('unread_num'))
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
            'delta_time': convertTimeDeltaToDayHourMinString(time_delta),
            'title': log.title,
            'log': log.log,
            'type': log.type,
        })

    MessageLog.objects.filter(time__lte=now).update(read=True)


    context = {
        'messagelog_data': messagelog_data
    }
    return render(request, 'template_dashboard/update_message_log_code_piece.html', context)
