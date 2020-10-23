from django.shortcuts import render
from ..models import *

def forgot_password(request):

    context = {

    }
    return render(request, 'template_dashboard/forgot_password.html', context)
