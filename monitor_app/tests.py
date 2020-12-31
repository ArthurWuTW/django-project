# WARNING before running the script below, make sure the db account has the permission
# to create database (because in testing, django creates a db and destroy it after testing)
# > python3 manage.py test

# the command to allow account to create db
# > sudo -u postgres psql
# > ALTER USER <django-db-account> CREATEDB;

import glob
from os.path import dirname, basename, join
tests_collection = glob.glob(join(dirname(__file__), "tests_collection", "*.py"))
for f in tests_collection:
    import_script =\
"""\
from .{0}.{1} import *\
""".format("tests_collection", basename(f[:-3]).replace('/', '.'))
    # print(import_script)
    exec (import_script)
