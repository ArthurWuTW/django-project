import glob
from os.path import dirname, basename, join
views_collection = glob.glob(join(dirname(__file__), "views_collection", "*.py"))
for f in views_collection:
    import_script =\
"""\
from .{0}.{1} import *\
""".format("views_collection", basename(f[:-3]).replace('/', '.'))
    print(import_script)
    exec (import_script)
