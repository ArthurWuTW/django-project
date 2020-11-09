from django.shortcuts import render, redirect
from ..models import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
import sys
import os


def updateLogMessage(request):
    context = {
    }
    return render(request, 'template_dashboard/update_message_log_code_piece.html', context)
