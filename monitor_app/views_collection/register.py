from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ..models import *

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
