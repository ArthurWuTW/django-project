from django.shortcuts import render
from ..models import *
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta

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
from django.http import JsonResponse

class UpdateConnectionsView(View):
    def post(self, request):
        server_name = request.POST.get('server_name')
        now = datetime.now()
        threshold_timestamp = now - timedelta(hours=48)
        connHandler = ConnectionHandler()
        connHandler.setQueryServerName(server_name)
        connHandler.setTitle("data")
        connHandler.setTimezoneShift(timedelta(hours=8))
        connHandler.setThresholdTimestamp(threshold_timestamp)

        contextHandler = ContextHandler()
        contextHandler.join(connHandler)
        contextHandler.fillInContext()
        return JsonResponse(contextHandler.getContext())
