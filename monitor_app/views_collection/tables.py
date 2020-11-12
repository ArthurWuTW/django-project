from django.shortcuts import render
from ..models import *
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from django.db import connection

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

def tables(request):

    now = datetime.now()

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

    # Message center
    message = list()
    unread_log_msg_num = 0
    if(request.user.is_authenticated):
        current_user = User.objects.get(username = request.user.username)
        print(current_user)
        profile = Profile.objects.get(user = current_user)
        print(profile.activated)
        if(profile.activated):
            unread_log_msg_num = len(MessageLog.objects.filter(user = current_user, read=False))
            log_msg = MessageLog.objects.filter(user = current_user).order_by('-time')[:unread_log_msg_num+5]
            print(log_msg)
            for log in log_msg:
                time_delta = now - log.time.replace(tzinfo=None)
                print(log.time)
                message.append({
                    'delta_time': convertTimeDeltaToDayHourMinString(time_delta),
                    'title': log.title,
                    'type': log.type,
                    'log': log.log,
                    'read': log.read
                })

    messagelog_data = dict()
    print("unread_log_msg_num", unread_log_msg_num)
    messagelog_data['unread_red_message_number'] = unread_log_msg_num
    messagelog_data['messagelog_array'] = message

    context = {
        'plant_table': json.dumps({
                                    'title': plant_table_title_list,
                                    'data': plant_table_row_list}),
        'messagelog_data': json.dumps(messagelog_data),
    }
    return render(request, 'template_dashboard/tables.html', context)
