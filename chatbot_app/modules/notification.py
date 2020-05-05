import django, os
os.environ.setdefault('DJANGO_SETTING_MODULE', 'ChatBot_Main.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ChatBot_Main.settings'
django.setup()
from chatbot_app.models import userDiagnosis
from django.utils import timezone
import requests, json, time, datetime, pytz

class Notification():
    def __init__(self):
        pass

    def checkin_date(self, period):
        print('Start Daemon Process: Checkin Notification.')
        while True:
            self.d_users = list(userDiagnosis.objects.all().values())
            for user in self.d_users:
                recorded_dt = user['datetime']
                diag_result = user['diagnosis_result']
                checkin = user['check_in']
                chat_id = user['chat_ID']
                current_dt = timezone.now()
                notify_dt = None
                if diag_result == '1':
                    notify_dt = recorded_dt + datetime.timedelta(days=2)
                elif diag_result == '2':
                    notify_dt = recorded_dt + datetime.timedelta(days=14)
                else:
                    print("diag_result is not either 1 or 2.")

                if notify_dt < current_dt and checkin == True:
                    self.send_checkin(chat_id, diag_result)
                    userDiagnosis.objects.filter(chat_ID=chat_id).update(check_in=False)
                    print("Sent Notification for checkin user!!")
            time.sleep(period)

    def send_checkin(self, chat_id, diag_result): 
        token = os.environ['bot_token']
        if diag_result == '1':
            text = "Heya, just checking in on your health condition. How's your symptoms now? Do you want to do self-assessment again?"
        else:
            text = "Heya, just checking in your status. Have you been isolating yourself from others? Now that 2-weeks quarantine is over, do you want to do another round of self-assessment?"
        reply_markup =  {"inline_keyboard": [[{"text": "Yes","callback_data": "Self Assessment"},{"text": "No","callback_data" : "Nope"}]]}
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
        
        req = requests.post(url, data = data)
        res = req.json()
        print(res)
        
