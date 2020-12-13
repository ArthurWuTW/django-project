from datetime import datetime, date
import json
from ...models import *
from termcolor import colored
import base64
import numpy as np
import cv2

class ImageHandler():
    def __init__(self):
        self.raw_data = None
        self.image = None
        self.now = None
        self.received_data = None

    def setNow(self, now):
        self.now = now

    def receiveEncodedRawData(self, request):
        self.received_data = json.loads(request.body.decode("utf-8"))
        self.raw_data = self.received_data['image']
        # encoding decoding processing
        self.raw_data = self.raw_data.encode("utf-8")
        # print(raw_data)

    def decodeRawDataToImage(self):

        imgString = base64.b64decode(self.raw_data)
        np_array = np.fromstring(imgString, np.uint8)
        # print(np_array)

        self.image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    def updatePlantData(self):
        django_path = '../'
        image_dir = 'data_image/'
        image_name = self.now.strftime("%Y_%m_%d_")+str(self.received_data['id'])+'.jpg'
        cv2.imwrite(django_path+image_dir+image_name, self.image)
        print(colored('[VIEW LOG] receiveImage - Image saved.', 'yellow', attrs=['bold']))

        if(PlantData.objects.filter(image_url=image_name).exists() == False):
            plant_data = PlantData()
            plant_data.aruco_id = self.received_data['id']
            plant_data.image_url = image_name
            plant_data.type = "N/A"
            plant_data.growth_rate = 0.0
            plant_data.seed_date = datetime.strptime('2020-10-29', '%Y-%m-%d').date()
            plant_data.data_date = date.today()
            plant_data.status = "N/A"
            plant_data.save()
            print(colored('[VIEW LOG] receiveImage - PlantData saved.', 'yellow', attrs=['bold']))

    def store3dContructImage(self):
        django_path = '../'
        image_dir = 'data_3dConstruction_image/'
        image_name = self.now.strftime("%Y_%m_%d_")+str(self.received_data['id'])+'.jpg'
        cv2.imwrite(django_path+image_dir+image_name, self.image)
        print(colored('[VIEW LOG] store3dContructImage - Image saved.', 'yellow', attrs=['bold']))
