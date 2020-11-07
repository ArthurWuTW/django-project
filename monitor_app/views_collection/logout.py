from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as auth_logout
from ..models import *

def logout(request):
    auth_logout(request)
    print(request.user)
    return redirect('/')
