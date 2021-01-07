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
from django.views.decorators.csrf import csrf_exempt

path = "...." # directory - django_project (outest one)
from secure_data.secure_data_loader import SecureDataLoader

from django.views import View

import glob
from os.path import dirname, basename, join
handlers_collection = glob.glob(join(dirname(__file__), "handlers", "*.py"))
for f in handlers_collection:
    import_script =\
"""\
from .{0}.{1} import *\
""".format("handlers", basename(f[:-3]).replace('/', '.'))
    # print(import_script)
    exec (import_script)

import requests

class Register(View):
    @csrf_exempt
    def post(self, request):
        secure_data_loader = SecureDataLoader()
        authHandler = AuthenticationHandler()
        contextHandler = ContextHandler()
        contextHandler.join(authHandler)

        authHandler.check_same_password(request)
        if not authHandler.pwd_repeatPwd_is_same():
            contextHandler.fillInContext()
            return render(request, 'template_dashboard/register.html', contextHandler.getContext())

        authHandler.check_same_username(request)
        if not authHandler.has_username_exists():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': secure_data_loader.secure_data['RECAPTCHA_PRIVATE_KEY'],
                'response': recaptcha_response
            }
            verify_rs = requests.get(url, params=values, verify=True)
            verify_rs = verify_rs.json()
            print(verify_rs)
            ''' End reCAPTCHA validation '''
            ''' Account length check start '''
            email_check_flag = True
            email_user = request.POST.get('email', '').split('@')
            # TODO use regular expression
            for substring in email_user:
                if len(substring)>20:
                    email_check_flag = False
            if not email_user[0].isalnum():
                email_check_flag = False

            print("email", email_user)
            ''' Account length check end '''

            print("verify_rs['success']", verify_rs['success'], "email_check_flag", email_check_flag )
            if verify_rs['success'] and email_check_flag:

                user = authHandler.createUserAndProfile(request)

                sender = MailSender()
                sender.setSubject("Activate Account")
                sender.setSmtpAccount(secure_data_loader.secure_data['SMTP_ACCOUNT'])
                sender.setSendTo(user.email)
                sender.setEmailTemplate("../templates/activation_email_template.txt")
                sender.setConfig({
                    "email":user.email,
                    'domain':secure_data_loader.secure_data['DOMAIN'],
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https',
                })
                sender.sendMail(secure_data_loader.secure_data['SMTP_ACCOUNT'], secure_data_loader.secure_data['SMTP_PASSWORD'])
                authHandler.updateStatus("Please click on the that has just been sent to your email account to verify your email and continue the registration process.")
                contextHandler.fillInContext()
                return render(request, 'template_dashboard/message_template.html', contextHandler.getContext())
            else:
                print("reCAPTCHA failed")
                authHandler.updateStatus("reCAPTCHA failed")
                contextHandler.fillInContext()
                return render(request, 'template_dashboard/register.html', contextHandler.getContext())
        else:
            authHandler.updateStatus("The email already exists!")
            contextHandler.fillInContext()
            return render(request, 'template_dashboard/register.html', contextHandler.getContext())

    def get(self, request):
        context = {
            'status_message': 'Create an Account'
        }
        return render(request, 'template_dashboard/register.html', context)
