from django.shortcuts import render
from ..models import *
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User

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

def dashboard(request):

    now = datetime.now()

    print('request.user.is_authenticated()', request.user.is_authenticated)
    time_threshold = datetime.now() - timedelta(hours=8)
    # gte : greater than equal
    temps = Temperature.objects.filter(time__gte=(time_threshold))
    humids = Humidity.objects.filter(time__gte=(time_threshold))

    temp_array_dict = dict()
    temp_array_dict['timestamp_array'] = [(temp.time + timedelta(hours=8)).strftime('%m/%d %H:%M') for temp in temps]
    temp_array_dict['temp_array'] = [temp.temperature for temp in temps]
    print('temp_array_dict', temp_array_dict)

    humid_array_dict = dict()
    humid_array_dict['timestamp_array'] = [(humid.time + timedelta(hours=8)).strftime('%m/%d %H:%M') for humid in humids]
    humid_array_dict['humid_array'] = [humid.humidity for humid in humids]
    print('humid_array_dict', humid_array_dict)

    cpu_temp = CpuTemperature.objects.get(id=1)
    cpu_data = {
        'timestamp': cpu_temp.time,
        'temperature': cpu_temp.cpuTemperature
    }

    latest_timePrice = TimePrice.objects.filter(
        product = "water_spinach"
    ).last()
    time_price_data = {
        'timestamp': (latest_timePrice.time + timedelta(hours=8)).strftime('%Y/%m/%d'),
        'price': latest_timePrice.price,
        'product': latest_timePrice.product
    }

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
    plants_data = dict()
    plants_data['plants'] = plant_array

    # Message center
    message = list()
    if(request.user.is_authenticated):
        current_user = User.objects.get(username = request.user.username)
        print(current_user)
        profile = Profile.objects.get(user = current_user)
        print(profile.activated)
        if(profile.activated):
            log_msg = MessageLog.objects.filter(user = current_user)
            print(log_msg)
            for log in log_msg:
                time_delta = now - log.time.replace(tzinfo=None)
                print(log.time)
                message.append({
                    'delta_time': convertTimeDeltaToDayHourMinString(time_delta),
                    'title': log.title,
                    'log': log.log,
                    'read': log.read
                })

    print(message)
    messagelog_data = dict()
    messagelog_data['messagelog_array'] = message
    messagelog_data['red_message_number'] = len(message)

    context = {
        'messagelog_data': json.dumps(messagelog_data),
        'plants_data': json.dumps(plants_data),
        'temp_data': json.dumps(temp_array_dict),
        'humid_data': json.dumps(humid_array_dict),
        'cpu_data': cpu_data,
        'time_price': time_price_data
    }
    return render(request, 'template_dashboard/dashboard.html', context)
