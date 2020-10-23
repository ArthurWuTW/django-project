from django.http import HttpResponse
from ..models import *
from datetime import datetime


def timePrice(request, price, date, product):
    data = TimePrice()
    data.price = price
    data.time = datetime.strptime(date, "%Y_%m_%d")
    data.product = product
    data.save()

    return HttpResponse('')
