from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from ..models import *

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

from django.views import View

class Login(View):
    def get(self, request):
        context = {
            'status_message': 'Welcome Back'
        }
        return render(request, 'template_dashboard/login.html', context)
    def post(self, request):
        authHandler = AuthenticationHandler()
        authHandler.login(request)

        contextHandler = ContextHandler()
        contextHandler.join(authHandler)

        if(authHandler.has_loggedin):
            return redirect('/')
        else:
            contextHandler.fillInContext()
            return render(request, 'template_dashboard/login.html', contextHandler.getContext())
