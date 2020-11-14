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

class UpdateWarningCount(View):
    def get(self, request, status):
        taskHandler = WarningStatusHander()
        taskHandler.updateStatusData(status)

        return HttpResponse('succeed')
