from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.models import userList, userDiagnosis
from django.utils import timezone

class UserDB(Server):
    def __init__(self, request):
        super().__init__(request)
        self.first_name = super().rcvUserData('first_name')
        self.chat_ID = super().rcvUserData('id')

    def storeId(self):
        dict = {'first_name' : self.first_name,
                'chat_ID' : self.chat_ID
                }
        try:
            userList.objects.create(**dict) #use ** to add dict into models
            print('New user added.')
        except Exception as e: 
            print('Error: '+str(e) + '. User already exist. Skip')
    
    def subscribe(self):
        userList.objects.filter(chat_ID=self.chat_ID).update(subscribe=True)

        self.main_text = f"Thanks for sub, {self.first_name}! We will let you know if there is any announcement. 😁"
        return super().sendMsg(get_fb=True, single=True)

    def unsubscribe(self):
        userList.objects.filter(chat_ID=self.chat_ID).update(subscribe=False)
        self.main_text = f"I'm sorry to see you go, {self.first_name}! If you want to subscribe again, just click here /subscribe ❤️"
        return super().sendMsg(get_fb=True, single=True)

    def checkin(self):
        period = None
        checkin = super().rcvParam('Rating')
        # update user checkin in database
        result = userDiagnosis.objects.get(chat_ID=self.chat_ID).diagnosis_result
        #print("result: {}".format(result))
        if result == '2':
            period = 'weeks'
        elif result == '1':
            period = 'days'

        if checkin == "👍":
            #print("chatID: " + str(self.chat_ID))
            userDiagnosis.objects.filter(chat_ID=self.chat_ID).update(check_in=True, datetime=timezone.now())
            self.main_text = f"Ok, {self.first_name}! I will remind you again, so please check for notification after 2 "+ str(period) + " 😁"
            
        elif checkin == "👎":
            userDiagnosis.objects.filter(chat_ID=self.chat_ID).update(check_in=False)
            self.main_text = f"No problem, {self.first_name}. Do ask me again for self assessment anytime 😁"

        else:
            self.main_text = "I don't understand. Please select from either yes or no button! 😁"

        return super().sendMsg(get_fb=False, single=True)