from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.models import userList


class subscribe(Server):
    def __init__(self, request):
        super().__init__(request)
    
    def sub(self):
        first_name = super().rcvFirstName()
        chat_ID = super().rcvChatID()
        userList.objects.filter(chat_ID=chat_ID).update(subscribe=True)

        self.main_text = f"Thanks for sub,  {first_name}! We will let you know if there is any announcement. 😁"
        return super().sendMsg()

    def unsub(self):
        first_name = super().rcvFirstName()
        chat_ID = super().rcvChatID()
        userList.objects.filter(chat_ID=chat_ID).update(subscribe=False)
        self.main_text = f"No prob, {first_name}! If you want to subscribe to our announcement, just click here /subscribe ❤️"
        return super().sendMsg()
