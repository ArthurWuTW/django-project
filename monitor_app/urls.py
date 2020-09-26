from django.urls import path, include
from . import views

from . import converters
from django.urls import register_converter
register_converter(converters.FloatConverter, 'float')

urlpatterns = [
    path('',
        views.dashboard,
        name='dashboard'),
    path('temperature/<float:temp>',
        views.temperature,
        name='temperature'),
    path('humidity/<float:humid>',
        views.humidity,
        name='humidity'),
    path('cpuTemperature/<float:cpuTemp>',
        views.cpuTemperature,
        name='cpuTemperature'),
    path('receiveImage',
        views.receiveImage,
        name='receiveImage'),
    path('timePrice/<float:price>/date/<str:date>/product/<str:product>',
        views.timePrice,
        name='timePrice'),
]
