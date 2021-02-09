import datetime
import threading
import time
from termcolor import colored
import signal
import os
import json
import requests
import sys

sys.path.append("..")
from secure_data.secure_data_loader import SecureDataLoader
secure_data_loader = SecureDataLoader()

stop = False

def signal_handler(signal, frame):
    global stop
    print_str = '[] Ctrl+C KeyboardInterupt'
    print(colored(print_str, 'blue', attrs=['bold']))
    stop = True

def job():
    while not stop:
        # Do Update Cache
        print(colored('[Cache LOG] UpdateCache process starts', 'blue', attrs=['bold']))
        data = {
            'raspberry_secret_key':  secure_data_loader.secure_data['RASPBERRY_SECRET_KEY']
        }
        headers = {'content-type': 'application/json'}
        r = requests.post("https://plantmonitor.mooo.com/updateCache", data=json.dumps(data), headers=headers)
        print(colored('[Cache LOG] UpdateCache process finished', 'blue', attrs=['bold']))
        time.sleep(60)
if __name__ == '__main__':

    t = threading.Thread(target = job)
    t.start()

    print(colored('[Cache LOG] Thread process starts', 'blue', attrs=['bold']))

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
