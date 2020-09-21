from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from .fill_data import *
from datetime import datetime

# Create your views here.
def dashboard(request):
    context = {
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
