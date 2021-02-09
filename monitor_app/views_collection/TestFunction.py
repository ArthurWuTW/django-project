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

class TestFunction(View):
    def post(self, request):

        return HttpResponse('123')

    def get(self, request):
        return HttpResponse('gggggg')
