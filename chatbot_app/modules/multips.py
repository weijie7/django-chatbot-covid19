import multiprocessing, os
from chatbot_app.modules.notification import Notification
import requests, json, time, datetime, pytz

def start_ps(period = 5):
    ntf = Notification()
    p1 = multiprocessing.Process(target=ntf.checkin_date, args=(period, ))
    p1.daemon = True
    p1.start()
    print("Parent Process PID: " + str(os.getpid()))
    print('Start Multiprocess Process')

#start_ps()


from rq import Queue
from worker import conn
ntf = Notification()
q = Queue(connection = conn, default_timeout=5000)

while True:
    comment = q.enqueue(ntf.checkin_date)
    time.sleep(5)