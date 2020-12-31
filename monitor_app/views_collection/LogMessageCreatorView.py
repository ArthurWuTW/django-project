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

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from secure_data.secure_data_loader import SecureDataLoader

@method_decorator(csrf_exempt, name='dispatch')
class LogMessageCreatorView(View):
    def get(self, request, title, msg, type):
        msgHandler = MessageCenterHandler(request)
        msgHandler.createAuthorLogMessage(title, msg, type)

        return HttpResponse('succeed')
    def post(self, request):
        secure_data_loader = SecureDataLoader()
        received_data = json.loads(request.body.decode("utf-8"))
        print(received_data)
        if(received_data['raspberry_secret_key'] == secure_data_loader.secure_data['RASPBERRY_SECRET_KEY']):
            msgHandler = MessageCenterHandler(request)
            msgHandler.createAuthorLogMessage(received_data['title'], received_data['msg'], received_data['type'])
            return HttpResponse('succeed')
        else:
            return HttpResponse('wrong secret key')
