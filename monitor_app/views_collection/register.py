from django.shortcuts import render, redirect
from ..models import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

path = "...." # directory - django_project (outest one)
from secure_data.secure_data_loader import SecureDataLoader

def register(request):

    if(request.method == 'POST'):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')

        if(password != repeat_password):
            context = {
                'status_message': 'Repeat Password is not the same as Password!'

            }
            return render(request, 'template_dashboard/register.html', context)

        if not User.objects.filter(username=email).exists():
            user = User.objects.create_user(username=email,
                                            email=email,
                                            password=password)
            user.save()
            profile = Profile()
            profile.user = user
            profile.activation = False
            profile.save()

            # send verification email
            # -----
            subject = "Password Reset Requested"
            email_template_name = "../templates/activation_email_template.txt"
            c = {
                "email":user.email,
                'domain':'10.1.1.16:8000',
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }

            #Sending email
            content = MIMEMultipart()
            secure_data_loader = SecureDataLoader()
            content["subject"] = subject
            content["from"] = secure_data_loader.secure_data['SMTP_ACCOUNT']
            content["to"] = user.email
            content.attach(MIMEText(render_to_string(email_template_name, c)))

            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
                try:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login( secure_data_loader.secure_data['SMTP_ACCOUNT'],  secure_data_loader.secure_data['SMTP_PASSWORD'])
                    smtp.send_message(content)
                    print("Complete!")
                except Exception as e:
                    print("Error message: ", e)


            return redirect('accounts/login/')
        else:
            context = {
                'status_message': 'The email already exists!'
            }
            return render(request, 'template_dashboard/register.html', context)


    context = {
        'status_message': 'Create an Account'
    }
    return render(request, 'template_dashboard/register.html', context)
