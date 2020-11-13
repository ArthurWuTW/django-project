from django.urls import path, include
from . import views

from . import converters
from django.urls import register_converter
register_converter(converters.FloatConverter, 'float')

urlpatterns = [
    path('',
        views.Dashboard.as_view(),
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
    path('receiveImage',
        views.receiveImage,
        name='receiveImage'),
    path('activate/<str:uid>/<str:token>',
        views.activate,
        name='activate'),
    path('updateLogMessage',
        views.updateLogMessage,
        name='updateLogMessage'),
    path('writeLogMessage/<str:title>/<str:msg>/<str:type>',
        views.writeLogMessage,
        name='writeLogMessage'),
    path('updateCameraTask/<str:status>',
        views.updateCameraTask,
        name='updateCameraTask'),
    path('updatePiCpuTemperature/<str:status>',
        views.updatePiCpuTemperature,
        name='updatePiCpuTemperature'),
    path('updateWarningCount/<str:status>',
        views.updateWarningCount,
        name='updateWarningCount'),
    path('updateWateringStatus/<str:status>',
        views.updateWateringStatus,
        name='updateWateringStatus'),
    path('tables',
        views.Tables.as_view(),
        name='tables'),

]
