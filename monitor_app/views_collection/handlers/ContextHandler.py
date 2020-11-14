from django.shortcuts import render
from datetime import datetime, timedelta, date
import json
from django.contrib.auth.models import User
from .ModelDataHandler import ModelDataHandler
from ...models import *

class ContextHandler():
    def __init__(self):
        self.data_handler_list = list()
        self.context = {}
    def join(self, dataHandler):
        self.data_handler_list.append(dataHandler)
    def fillInContext(self):
        for data in self.data_handler_list:
            self.context[data.getTitle()] = data.getData()
    def clearContext(self):
        self.context = {}
    def getContext(self):
        return self.context
