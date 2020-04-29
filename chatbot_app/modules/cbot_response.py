from chatbot_app.modules.users_database import UserDB

# inhirit UserDB to use self.first_name member data
class CbotResponse(UserDB):
    def __init__(self, request):
        super().__init__(request)
    
    def goodbye(self):
        self.main_text = f"Thanks for using me, {self.first_name}! 😁"
        return super().sendMsg(get_fb=True, single=True)

    # can add more chatbot responses, e.g. welcome function with user name.