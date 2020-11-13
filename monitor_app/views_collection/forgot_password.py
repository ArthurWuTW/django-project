from django.shortcuts import render
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

def forgot_password(request):

    if not request.user.is_authenticated:

        if(request.method == 'POST'):
            email = request.POST.get('email', '')
            print("email", email)
            associated_users = User.objects.filter(email=email)
            print("associated_user", associated_users)
            if associated_users.exists():
                for user in associated_users:

                    subject = "Password Reset Requested"
                    email_template_name = "../templates/password_reset_email_template.txt"
                    c = {
                        "email":user.email,
                        'domain':secure_data_loader.secure_data['DOMAIN'],
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

            context = {
                'status_message': "Please click on the that has just been sent to your email account to change your password."
            }
            return render(request, 'template_dashboard/message_template.html', context)
        else:
            context = {

            }
            return render(request, 'template_dashboard/forgot_password.html', context)
    else:
        context = {
            'status_message': "You have already logged in."
        }
        return render(request, 'template_dashboard/message_template.html', context)
