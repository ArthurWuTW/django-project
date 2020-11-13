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

# path = "...." # directory - django_project (outest one)
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

class ForgotPassword(View):
    def post(self, request):
        secure_data_loader = SecureDataLoader()
        sender = MailSender()
        authHandler = AuthenticationHandler()
        authHandler.forgot_password(request)
        if authHandler.getForgotPwdUserObjectList().exists():
            for user in authHandler.getForgotPwdUserObjectList():

                sender.setSubject("Password Reset Requested")
                sender.setSmtpAccount(secure_data_loader.secure_data['SMTP_ACCOUNT'])
                sender.setSendTo(user.email)
                sender.setEmailTemplate("../templates/password_reset_email_template.txt")
                sender.setConfig({
                    "email":user.email,
                    'domain':secure_data_loader.secure_data['DOMAIN'],
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                })
                sender.sendMail(secure_data_loader.secure_data['SMTP_ACCOUNT'], secure_data_loader.secure_data['SMTP_PASSWORD'])
                context = {
                    'status_message': "Please click on the that has just been sent to your email account to change your password."
                }
                return render(request, 'template_dashboard/message_template.html', context)
    def get(self, request):
        if not request.user.is_authenticated:
            context = {

            }
            return render(request, 'template_dashboard/forgot_password.html', context)
        else:
            context = {
                'status_message': "You have already logged in."
            }
            return render(request, 'template_dashboard/message_template.html', context)
