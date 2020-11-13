from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from .ModelDataHandler import ModelDataHandler
from ...models import *

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


class AuthenticationHandler(ModelDataHandler):
    def __init__(self):
        self.status = None
    def activate(self, request, uid, token):
        uid = force_text(urlsafe_base64_decode(uid))
        try:
            user = User.objects.get(pk = uid)
            print(user)
        except User.DoesNotExist:
            user = None
            ERROR("activate.py : User does not exist!")

        if user and default_token_generator.check_token(user, token):
            profile = Profile.objects.get(user = user)
            profile.activation = True
            profile.save()

        self.status = "Your account has been successfully activated!"
    def getData(self):
        return self.status
    def getTitle(self):
        return 'status_message'
