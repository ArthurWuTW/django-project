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
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout

class AuthenticationHandler(ModelDataHandler):
    def __init__(self):
        self.status = None
        self.login_flag = False
        self.user_exits = False
        self.user_object_queryset_list = None
        self.repeat_password_is_same = None
        self.register_completed = False
        self.email_is_same = None
    def check_same_password(self, request):
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if(password == repeat_password):
            self.repeat_password_is_same = True
        else:
            self.repeat_password_is_same = False
            self.status = 'Repeat Password is not the same as Password!'
    def pwd_repeatPwd_is_same(self):
        return self.repeat_password_is_same
    def check_same_username(self, request):
        email = request.POST.get('email', '')
        if User.objects.filter(username=email).exists():
            self.email_is_same = True
        else:
            self.email_is_same = False
    def has_username_exists(self):
        return self.email_is_same
    def createUserAndProfile(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = User.objects.create_user(username=email,
                                        email=email,
                                        password=password)
        user.save()
        profile = Profile()
        profile.user = user
        profile.activation = False
        profile.save()
        return user

    def resetPassword(self, request, uid, token):
        new_password = request.POST.get('password', '')
        user = None
        uid = force_text(urlsafe_base64_decode(uid))
        try:
            user = User.objects.get(pk = uid)
        except User.DoesNotExist:
            user = None
        if user and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()

    def checkUidToken(self, uid, token):
        user = None
        uid = force_text(urlsafe_base64_decode(uid))
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None
            ERROR("activate.py : User does not exist!")
        if user and default_token_generator.check_token(user, token):
            return True
        else:
            return False

    def activate(self, uid, token):
        user = None
        uid = force_text(urlsafe_base64_decode(uid))
        try:
            user = User.objects.get(pk = uid)
            print(user)
        except User.DoesNotExist:
            user = None
            ERROR("activate.py : User does not exist!")

        if user and default_token_generator.check_token(user, token):
            profile = Profile.objects.get(user = user)
            profile.activated = True
            profile.save()
        self.status = "Your account has been successfully activated!"
    def login(self, request):
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            self.login_flag = True
        else:
            self.login_flag = False
            self.status = 'Login Failed'
    def logout(self, request):
        auth_logout(request)
        self.login_flag = False
    def forgot_password(self, request):
        email = request.POST.get('email', '')
        print("email", email)
        self.user_object_queryset_list = User.objects.filter(email=email)
        print("associated_user", self.user_object_queryset_list)
    def getForgotPwdUserObjectList(self):
        return self.user_object_queryset_list
    def getData(self):
        return self.status
    def getTitle(self):
        return 'status_message'
    def has_loggedin(self):
        return self.login_flag
    def updateStatus(self, status):
        self.status = status
