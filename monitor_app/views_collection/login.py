from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from ..models import *

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
