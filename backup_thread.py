import datetime
import threading
import time
from termcolor import colored
import signal
import os

stop = False

def signal_handler(signal, frame):
    global stop
    print_str = '[] Ctrl+C KeyboardInterupt'
    print(colored(print_str, 'yellow', attrs=['bold']))
    stop = True

def job():
    count_hours = 0
    while not stop:
        count_hours +=1
        print_str = '[BACKUP LOG] Hours Count = '+str(count_hours)
        print(colored(print_str, 'yellow', attrs=['bold']))
        time.sleep(60*60)

        if(count_hours == 24):
            # Do Backup
            print(colored('[BACKUP LOG] Backup process starts', 'yellow', attrs=['bold']))
            os.system('python3 ../backup_git.py')


            # Reset Count
            count_hours = 0


if __name__ == '__main__':

    t = threading.Thread(target = job)
    t.start()

    print(colored('[BACKUP LOG] Thread process starts', 'yellow', attrs=['bold']))

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
