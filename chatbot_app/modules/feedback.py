from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.models import feedbackList

class feedback(Server):
    def __init__(self, request):
        super().__init__(request)
    
    def store_fb(self):
        intent = super().rcvIntent()
        first_name = super().rcvFirstName()
        user_name = super().rcvUserName()
        session = self.req.get('session').split('/')[-1]
        rating = super().rcvParam('Rating')
        question = super().rcvParam('question')
        answer = super().rcvParam('answer')

        if rating == "👍":
            self.main_text = "Thank you for your input! ❤️"
            rating = 1
        elif rating == "👎":
            self.main_text = "Thanks for the feedback! I'm sorry you felt that way. We will look into this to improve! ❤️"
            rating = 0
        else:
            self.main_text = "I don't understand. Please select thumbs up/down from the button! 😁"
            rating = -1
        
        dict = {'intent' : intent,
                'first_name' : first_name,
                'telegram_user' : user_name,
                'session_ID' : session,
                'rating' : rating,
                'question' : question,
                'answer' : answer
                }
        feedbackList.objects.create(**dict) #use ** to add dict into models

        return super().feedbackMsg()