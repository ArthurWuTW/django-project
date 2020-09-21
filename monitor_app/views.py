from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
    context = {
    }
    return render(request, 'template_dashboard/dashboard.html', context)

def temperature(request, temp):

    #write into database
    

    return HttpResponse('')
