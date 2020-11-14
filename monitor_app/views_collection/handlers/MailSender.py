from django.shortcuts import render
from ...models import *
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

class MailSender():
    def __init__(self):
        #Sending email
        self.content = MIMEMultipart()
        self.template = ""
        self.config = {}
        self.mail_sended = False
    def setSubject(self, subject):
        self.content["subject"] = subject
    def setSmtpAccount(self, smtp):
        self.content["from"] = smtp
    def setSendTo(self, to):
        self.content["to"] = to
    def setEmailTemplate(self, path):
        self.template = path
    def setConfig(self, config):
        self.config = config
    def sendMail(self, account, pwd):
        self.content.attach(MIMEText(render_to_string(self.template, self.config)))
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(account, pwd)
                smtp.send_message(self.content)
                print("Complete!")
                self.mail_sended = True
            except Exception as e:
                print("Error message: ", e)
    def has_sent(self):
        return self.mail_sended
