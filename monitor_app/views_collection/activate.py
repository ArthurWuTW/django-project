from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ..models import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

def activate(request, uid, token):
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





    context = {
        'status_message': "Your account has been successfully activated!"
    }

    return render(request, 'template_dashboard/message_template.html', context)
