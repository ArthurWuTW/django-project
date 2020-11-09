from django.urls import path, include
from . import views

from . import converters
from django.urls import register_converter
register_converter(converters.FloatConverter, 'float')

urlpatterns = [
    path('',
        views.dashboard,
        name='dashboard'),
    path('accounts/login/', # replace auth.accounts.login
        views.login,
        name='login'),
    path('accounts/logout/',
        views.logout,
        name='logout'),
    path('register',
        views.register,
        name='register'),
    path('forgot_password',
        views.forgot_password,
        name='forgot_password'),
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
    path('activate/<str:uid>/<str:token>',
        views.activate,
        name='activate'),
    path('updateLogMessage',
        views.updateLogMessage,
        name='updateLogMessage'),
    path('writeLogMessage/<str:title>/<str:msg>/<str:type>',
        views.writeLogMessage,
        name='writeLogMessage'),
]
