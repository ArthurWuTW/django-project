from django.shortcuts import render
from ..models import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

def forgot_password(request):
    if(request.method == 'POST'):
        email = request.POST.get('email', '')
        print("email", email)
        associated_user = User.objects.filter(email=email)
        print("associated_user", associated_user)
        if associated_user.exists():
            #Sending email


    # if post
    #     gemerate token
    #     send email

    context = {

    }
    return render(request, 'template_dashboard/forgot_password.html', context)
