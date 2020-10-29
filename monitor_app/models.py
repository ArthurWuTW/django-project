import glob
from os.path import dirname, basename, join
models_collection = glob.glob(join(dirname(__file__), "models_collection", "*.py"))
for f in models_collection:
    import_script =\
"""\
from .{0}.{1} import *\
""".format("models_collection", basename(f[:-3]).replace('/', '.'))
    print(import_script)
    exec (import_script)
