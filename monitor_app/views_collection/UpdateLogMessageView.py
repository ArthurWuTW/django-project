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

class UpdateLogMessageView(View):
    def post(self, request):
        msgUpdateHandler = UpdateMessageHandler(request)
        contextHandler = ContextHandler()
        contextHandler.join(msgUpdateHandler)
        contextHandler.fillInContext()
        return render(request, 'template_dashboard/update_message_log_code_piece.html', contextHandler.getContext())
