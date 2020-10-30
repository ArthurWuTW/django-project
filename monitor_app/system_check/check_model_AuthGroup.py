from ..models import *
from termcolor import colored

class CheckAuthGroup():
    def __init__(self):
        self.check_list = ["Viewer", "Author"]
    def system_check(self):
        for group in self.check_list:
            try:
                auth_group = AuthGroup.objects.get(group=group)
            except AuthGroup.DoesNotExist:
                print(str(group)+" is not in AuthGroup!")
        assert len(AuthGroup.objects.all()) == len(self.check_list)
        print(colored('[OK] CheckAuthGroup system check pass', 'green', attrs=['bold']))
