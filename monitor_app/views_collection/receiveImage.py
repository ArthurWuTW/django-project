from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import *
from datetime import datetime
import json

@csrf_exempt
def receiveImage(request):

    if request.method == 'POST':

        received_data = json.loads(request.body.decode("utf-8"))

        raw_data = received_data['image']
        print("------------------------")
        # encoding decoding processing
        raw_data = raw_data.encode("utf-8")
        print(raw_data)

        import base64
        import numpy as np
        import cv2

        imgString = base64.b64decode(raw_data)
        np_array = np.fromstring(imgString, np.uint8)
        print(np_array)

        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        print(image)



        # growth_data
        # growth_data = received_data['data']
        # now = datetime.now()
        # for data in growth_data:
        #     growth_object = GrowthRate()
        #     growth_object.time = now
        #     growth_object.plant_id = data['id']
        #     growth_object.rate = data['growth_rate']
        #     growth_object.save()

        django_path = '../'
        image_dir = 'data_image/'
        image_name = now.strftime("%Y_%m_%d")+str(received_data['id'])+'.jpg'

        print(django_path+image_dir+image_name)

        cv2.imwrite(django_path+image_dir+image_name, image)

        return HttpResponse(str(received_data))

    return HttpResponse('Not post')
