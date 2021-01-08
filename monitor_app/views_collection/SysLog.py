from django.shortcuts import render
from ..models import *
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from django.db import connection
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

class SysLog(View):
    def get(self, request):
        now = datetime.now()
        threshold_timestamp = now - timedelta(hours=48)

        now = datetime.now()
        connHandler = ConnectionHandler()
        connHandler.setQueryServerName("Backup")
        connHandler.setTimezoneShift(timedelta(hours=8))
        connHandler.setThresholdTimestamp(threshold_timestamp)


        messageHandler = MessageCenterHandler(self.request)
        messageHandler.setNow(now)

        contextHandler = ContextHandler()
        contextHandler.join(messageHandler)
        contextHandler.join(connHandler)

        contextHandler.fillInContext()
        
        return render(self.request, 'template_dashboard/sysLog.html', contextHandler.getContext())
