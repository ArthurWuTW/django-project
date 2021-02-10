from django.http import HttpResponse
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
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from secure_data.secure_data_loader import SecureDataLoader
import requests
import os

@method_decorator(csrf_exempt, name='dispatch')
class UpdateCache(View):
    def post(self, request):
        secure_data_loader = SecureDataLoader()
        received_data = json.loads(request.body.decode("utf-8"))
        print(received_data)
        if('raspberry_secret_key' in received_data and received_data['raspberry_secret_key'] == secure_data_loader.secure_data['RASPBERRY_SECRET_KEY']):
            now = datetime.now()
            threshold_timestamp = now - timedelta(hours=48)
            connHandler = ConnectionHandler()
            connHandler.setQueryServerName("Backup")
            connHandler.setTitle("connections_data")
            connHandler.setTimezoneShift(timedelta(hours=8))
            connHandler.setThresholdTimestamp(threshold_timestamp)
            connHandler.writeCacheData(cache)

            connHandler_private_server = ConnectionHandler()
            connHandler_private_server.setQueryServerName("PrivateServer")
            connHandler_private_server.setTitle("connections_data_private_server")
            connHandler_private_server.setTimezoneShift(timedelta(hours=8))
            connHandler_private_server.setThresholdTimestamp(threshold_timestamp)
            connHandler_private_server.writeCacheData(cache)

            connHandler_backup_cpu = ConnectionHandler()
            connHandler_backup_cpu.setQueryServerName("BackupCpuPercentage")
            connHandler_backup_cpu.setTitle("connections_data_backup_cpu")
            connHandler_backup_cpu.setTimezoneShift(timedelta(hours=8))
            connHandler_backup_cpu.setThresholdTimestamp(threshold_timestamp)
            connHandler_backup_cpu.writeCacheData(cache)

            connHandler_backup_mem = ConnectionHandler()
            connHandler_backup_mem.setQueryServerName("BackupMemPercentage")
            connHandler_backup_mem.setTitle("connections_data_backup_mem")
            connHandler_backup_mem.setTimezoneShift(timedelta(hours=8))
            connHandler_backup_mem.setThresholdTimestamp(threshold_timestamp)
            connHandler_backup_mem.writeCacheData(cache)

            connHandler_webserver_cpu = ConnectionHandler()
            connHandler_webserver_cpu.setQueryServerName("WebServerCpuPercentage")
            connHandler_webserver_cpu.setTitle("connections_data_webserver_cpu")
            connHandler_webserver_cpu.setTimezoneShift(timedelta(hours=8))
            connHandler_webserver_cpu.setThresholdTimestamp(threshold_timestamp)
            connHandler_webserver_cpu.writeCacheData(cache)

            connHandler_webserver_mem = ConnectionHandler()
            connHandler_webserver_mem.setQueryServerName("WebServerMemPercentage")
            connHandler_webserver_mem.setTitle("connections_data_webserver_mem")
            connHandler_webserver_mem.setTimezoneShift(timedelta(hours=8))
            connHandler_webserver_mem.setThresholdTimestamp(threshold_timestamp)
            connHandler_webserver_mem.writeCacheData(cache)

            connHandler_private_server_ssh_failed = ConnectionHandler()
            connHandler_private_server_ssh_failed.setQueryServerName("PrivateServerSshFailed")
            connHandler_private_server_ssh_failed.setTitle("connections_data_private_server_ssh_failed")
            connHandler_private_server_ssh_failed.setTimezoneShift(timedelta(hours=8))
            connHandler_private_server_ssh_failed.setThresholdTimestamp(threshold_timestamp)
            connHandler_private_server_ssh_failed.writeCacheData(cache)

            connHandler_private_server_ssh_banned = ConnectionHandler()
            connHandler_private_server_ssh_banned.setQueryServerName("PrivateServerSshBanned")
            connHandler_private_server_ssh_banned.setTitle("connections_data_private_server_ssh_banned")
            connHandler_private_server_ssh_banned.setTimezoneShift(timedelta(hours=8))
            connHandler_private_server_ssh_banned.setThresholdTimestamp(threshold_timestamp)
            connHandler_private_server_ssh_banned.writeCacheData(cache)


            return HttpResponse('Conn Data Cache Updated!')
        else:
            return HttpResponse('wrong secret key')
