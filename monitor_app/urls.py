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
        views.Login.as_view(),
        name='login'),
    path('accounts/logout/',
        views.Logout.as_view(),
        name='logout'),
    path('register',
        views.Register.as_view(),
        name='register'),
    path('forgot_password',
        views.ForgotPassword.as_view(),
        name='forgot_password'),
    path('temperature/<float:temp>',
        views.TemperatureReceiver.as_view(),
        name='temperature'),
    path('humidity/<float:humid>',
        views.HumidityReceiver.as_view(),
        name='humidity'),
    path('receiveImage',
        views.ReceiveImage.as_view(),
        name='receiveImage'),
    path('activate/<str:uid>/<str:token>',
        views.Activate.as_view(),
        name='activate'),
    path('updateLogMessage',
        views.UpdateLogMessageView.as_view(),
        name='updateLogMessage'),
    path('writeLogMessage/<str:title>/<str:msg>/<str:type>',
        views.LogMessageCreatorView.as_view(),
        name='writeLogMessage'),
    path('updateCameraTask/<str:status>',
        views.UpdateCameraTask.as_view(),
        name='updateCameraTask'),
    path('updatePiCpuTemperature/<str:status>',
        views.UpdatePiCpuTemperature.as_view(),
        name='updatePiCpuTemperature'),
    path('updateWarningCount/<str:status>',
        views.UpdateWarningCount.as_view(),
        name='updateWarningCount'),
    path('updateWateringStatus/<str:status>',
        views.UpdateWateringStatus.as_view(),
        name='updateWateringStatus'),
    path('tables',
        views.Tables.as_view(),
        name='tables'),

]
