import multiprocessing, os
from chatbot_app.modules.notification import Notification

def start_ps(period = 5):
    ntf = Notification()
    p1 = multiprocessing.Process(target=ntf.checkin_date, args=(period, ))
    p1.daemon = True
    p1.start()
    print("Parent Process PID: " + str(os.getpid()))
    print('Start Multiprocess Process')

start_ps()
