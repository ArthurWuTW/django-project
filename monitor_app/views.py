from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from datetime import datetime, timedelta
from .view_utils import *
import json
import os

# Create your views here.
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

    context = {
        'temp_data': json.dumps(temp_array_dict),
        'humid_data': json.dumps(humid_array_dict),
        'cpu_data': cpu_data,
        'time_price': time_price_data
    }
    return render(request, 'template_dashboard/dashboard.html', context)

def temperature(request, temp):
    print("temp", temp)
    data = Temperature()
    data.temperature = temp
    data.time = datetime.now()
    print(data.temperature)
    print(data.time)
    data.save()

    return HttpResponse('')

def humidity(request, humid):
    print("humid", humid)
    data = Humidity()
    data.humidity = humid
    data.time = datetime.now()
    data.save()

    return HttpResponse('')

def cpuTemperature(request, cpuTemp):
    print("cpu temp", cpuTemp)
    data = CpuTemperature.objects.get(id=1)
    data.cpuTemperature = cpuTemp
    data.time = datetime.now()
    data.save()

    return HttpResponse('')

@csrf_exempt
def receiveImage(request):

    if request.method == 'POST':

        received_data = json.loads(request.body.decode("utf-8"))

        raw_data = received_data['image']
        print("------------------------")
        # encoding decoding processing
        raw_data = raw_data.encode("utf-8")
        print(raw_data)

        import base64
        import numpy as np
        import cv2

        imgString = base64.b64decode(raw_data)
        np_array = np.fromstring(imgString, np.uint8)
        print(np_array)

        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        print(image)



        # growth_data
        growth_data = received_data['data']
        now = datetime.now()
        for data in growth_data:
            growth_object = GrowthRate()
            growth_object.time = now
            growth_object.plant_id = data['id']
            growth_object.rate = data['growth_rate']
            growth_object.save()

        django_path = '../'
        image_dir = 'data_image/'
        image_name = now.strftime("%Y_%m_%d")+'.jpg'

        print(django_path+image_dir+image_name)

        cv2.imwrite(django_path+image_dir+image_name, image)

        return HttpResponse(str(received_data))

    return HttpResponse('Not post')

def timePrice(request, price, date, product):
    data = TimePrice()
    data.price = price
    data.time = datetime.strptime(date, "%Y_%m_%d")
    data.product = product
    data.save()

    return HttpResponse('')

def login(request):

    if(request.method == 'POST'):
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            return redirect('/')
        else:
            context = {
                'status_message': 'Login Failed'
            }
            return render(request, 'template_dashboard/login.html', context)


    context = {
        'status_message': 'Welcome Back'
    }
    return render(request, 'template_dashboard/login.html', context)

def register(request):

    if(request.method == 'POST'):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')

        if(password!=repeat_password):
            context = {
                'status_message': 'Repeat Password is not the same as Password!'

            }
            return render(request, 'template_dashboard/register.html', context)

        print("adf",email, password)

        if not User.objects.filter(username=email).exists():
            user = User.objects.create_user(username=email,
                                            email=email,
                                            password=password)
            user.save()

            return redirect('/login')
        else:
            context = {
                'status_message': 'The email already exists!'
            }
            return render(request, 'template_dashboard/register.html', context)


    context = {
        'status_message': 'Create an Account'
    }
    return render(request, 'template_dashboard/register.html', context)

def forgot_password(request):

    context = {

    }
    return render(request, 'template_dashboard/forgot_password.html', context)
