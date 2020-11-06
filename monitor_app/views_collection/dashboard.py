from django.shortcuts import render
from ..models import *
from datetime import datetime, timedelta, date
import json

def dashboard(request):
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

    context = {
        'plants_data': json.dumps(plants_data),
        'temp_data': json.dumps(temp_array_dict),
        'humid_data': json.dumps(humid_array_dict),
        'cpu_data': cpu_data,
        'time_price': time_price_data
    }
    return render(request, 'template_dashboard/dashboard.html', context)
