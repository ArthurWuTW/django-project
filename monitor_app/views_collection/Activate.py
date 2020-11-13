from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ..models import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
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

class Activate(View):
    def get(self, request, uid, token):
        authHandler = AuthenticationHandler()
        authHandler.activate(request, uid, token)

        contextHandler = ContextHandler()
        contextHandler.join(authHandler)
        contextHandler.fillInContext()

        return render(request, 'template_dashboard/message_template.html', contextHandler.getContext())
