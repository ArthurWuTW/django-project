from django.shortcuts import render
from ..models import *
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from django.db import connection
from django.views import View
from django.http import HttpResponse

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

class ResetPassword(View):
    def get(self, request, username, token):
        print(username, token)
        authHandler = AuthenticationHandler()
        if authHandler.checkUidToken(username, token):
            self.token = token
            self.username = username
            return render(self.request, 'template_selfdone/reset_password.html', {})
        else:
            return HttpResponse(status=500)

    def post(self, request, username, token):
        authHandler = AuthenticationHandler()
        authHandler.resetPassword(request, username, token)
        authHandler.updateStatus("Password has been reset, Please login again!")

        contextHandler = ContextHandler()
        contextHandler.join(authHandler)
        contextHandler.fillInContext()
        return render(request, 'template_dashboard/message_template.html', contextHandler.getContext())
