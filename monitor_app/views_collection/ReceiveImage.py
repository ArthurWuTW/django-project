from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import *
from datetime import datetime, date
import json
from termcolor import colored

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

class ReceiveImage(View):
    @csrf_exempt
    def post(self, request):
        now = datetime.now()
        imgHandler = ImageHandler()
        imgHandler.setNow(now)
        imgHandler.receiveEncodedRawData(request)
        imgHandler.decodeRawDataToImage()
        imgHandler.updatePlantData()

        return HttpResponse('Succeed')

# @csrf_exempt
# def receiveImage(request):
#
#     if request.method == 'POST':
#
#         received_data = json.loads(request.body.decode("utf-8"))
#
#         raw_data = received_data['image']
#         # encoding decoding processing
#         raw_data = raw_data.encode("utf-8")
#         # print(raw_data)
#
#         import base64
#         import numpy as np
#         import cv2
#
#         imgString = base64.b64decode(raw_data)
#         np_array = np.fromstring(imgString, np.uint8)
#         # print(np_array)
#
#         image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
#         # print(image)
#
#         now = datetime.now()
#         django_path = '../'
#         image_dir = 'data_image/'
#         image_name = now.strftime("%Y_%m_%d_")+str(received_data['id'])+'.jpg'
#         cv2.imwrite(django_path+image_dir+image_name, image)
#         print(colored('[VIEW LOG] receiveImage - Image saved.', 'yellow', attrs=['bold']))
#         # plant data
#         if(PlantData.objects.filter(image_url=image_name).exists() == False):
#             plant_data = PlantData()
#             plant_data.aruco_id = received_data['id']
#             plant_data.image_url = image_name
#             plant_data.type = "N/A"
#             plant_data.growth_rate = 0.0
#             plant_data.seed_date = datetime.strptime('2020-10-29', '%Y-%m-%d').date()
#             plant_data.data_date = date.today()
#             plant_data.status = "N/A"
#             plant_data.save()
#             print(colored('[VIEW LOG] receiveImage - PlantData saved.', 'yellow', attrs=['bold']))
#
#         return HttpResponse(str(received_data))
#
#     return HttpResponse('Not post')
