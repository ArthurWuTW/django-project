from django.http import HttpResponse
from ..models import *
from datetime import datetime

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

class HumidityReceiver(View):
    def get(self, request, humid):
        humidHandler = HumidityHandler()
        status = humidHandler.insertData(humid)
        return HttpResponse(status)