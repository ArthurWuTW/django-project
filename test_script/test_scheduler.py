import datetime
import schedule
import threading
import time

import threading
import time
def job():
    while True:
        print(time.ctime())
        time.sleep(5)

if __name__ == '__main__':

    t = threading.Thread(target = job)
    t.start()
    print("hey")
