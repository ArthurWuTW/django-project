from django.contrib import admin
from .models import *
import os

import glob
from os.path import dirname, basename, join
models_collection = [file for file in os.listdir(join(dirname(__file__), "models_collection")) if file.endswith(".py")]

for f in models_collection:
    import_script =\
"""\
admin.site.register({0})\
""".format(f[:-3])
    # print(import_script)
    exec (import_script)
