from django.apps import AppConfig


class MonitorAppConfig(AppConfig):
    name = 'monitor_app'
    def ready(self):

        #check AuthGroup
        from .system_check.check_model_AuthGroup import CheckAuthGroup
        check = CheckAuthGroup()
        check.system_check()
