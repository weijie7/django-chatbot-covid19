from chatbot_app.modules.dialogflow_msg import Server

class goodbye(Server):
    def __init__(self, request):
        super().__init__(request)
    
    def bye(self):
        first_name = super().rcvFirstName()
        self.main_text = f"Thanks for using me, {first_name}! 😁"
        self.get_input = 1
        return super().sendMsg()