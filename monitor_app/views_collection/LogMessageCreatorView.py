from django.http import HttpResponse
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from datetime import datetime, timedelta

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

class LogMessageCreatorView(View):
    def get(self, request, title, msg, type):
        msgHandler = MessageCenterHandler(request)
        msgHandler.createAuthorLogMessage(title, msg, type)

        return HttpResponse('succeed')
