from django.http import HttpResponse
from ..models import *
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
from secure_data.secure_data_loader import SecureDataLoader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class ConnectionsNumReceiver(View):
    def post(self, request):
        secure_data_loader = SecureDataLoader()
        received_data = json.loads(request.body.decode("utf-8"))
        print(received_data)
        print(received_data['raspberry_secret_key'])
        print(received_data['server_name'])
        if('raspberry_secret_key' in received_data and received_data['raspberry_secret_key'] == secure_data_loader.secure_data['RASPBERRY_SECRET_KEY']):
            print("pass")
            connsHandler = ConnectionHandler()
            status = connsHandler.insertData(received_data['server_name'], received_data['number'])
            return HttpResponse(status)
        else:
            return HttpResponse('wrong secret key')
