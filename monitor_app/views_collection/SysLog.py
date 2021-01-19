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
        connHandler = ConnectionHandler()
        connHandler.setQueryServerName("Backup")
        connHandler.setTitle("connections_data")
        connHandler.setTimezoneShift(timedelta(hours=8))
        connHandler.setThresholdTimestamp(threshold_timestamp)

        connHandler_private_server = ConnectionHandler()
        connHandler_private_server.setQueryServerName("PrivateServer")
        connHandler_private_server.setTitle("connections_data_private_server")
        connHandler_private_server.setTimezoneShift(timedelta(hours=8))
        connHandler_private_server.setThresholdTimestamp(threshold_timestamp)

        connHandler_backup_cpu = ConnectionHandler()
        connHandler_backup_cpu.setQueryServerName("BackupCpuPercentage")
        connHandler_backup_cpu.setTitle("connections_data_backup_cpu")
        connHandler_backup_cpu.setTimezoneShift(timedelta(hours=8))
        connHandler_backup_cpu.setThresholdTimestamp(threshold_timestamp)

        connHandler_backup_mem = ConnectionHandler()
        connHandler_backup_mem.setQueryServerName("BackupMemPercentage")
        connHandler_backup_mem.setTitle("connections_data_backup_mem")
        connHandler_backup_mem.setTimezoneShift(timedelta(hours=8))
        connHandler_backup_mem.setThresholdTimestamp(threshold_timestamp)

        connHandler_webserver_cpu = ConnectionHandler()
        connHandler_webserver_cpu.setQueryServerName("WebServerCpuPercentage")
        connHandler_webserver_cpu.setTitle("connections_data_webserver_cpu")
        connHandler_webserver_cpu.setTimezoneShift(timedelta(hours=8))
        connHandler_webserver_cpu.setThresholdTimestamp(threshold_timestamp)

        connHandler_webserver_mem = ConnectionHandler()
        connHandler_webserver_mem.setQueryServerName("WebServerMemPercentage")
        connHandler_webserver_mem.setTitle("connections_data_webserver_mem")
        connHandler_webserver_mem.setTimezoneShift(timedelta(hours=8))
        connHandler_webserver_mem.setThresholdTimestamp(threshold_timestamp)



        messageHandler = MessageCenterHandler(self.request)
        messageHandler.setNow(now)

        contextHandler = ContextHandler()
        contextHandler.join(messageHandler)
        contextHandler.join(connHandler)
        contextHandler.join(connHandler_private_server)
        contextHandler.join(connHandler_backup_cpu)
        contextHandler.join(connHandler_backup_mem)
        contextHandler.join(connHandler_webserver_cpu)
        contextHandler.join(connHandler_webserver_mem)
        contextHandler.fillInContext()

        return render(self.request, 'template_dashboard/sysLog.html', contextHandler.getContext())
