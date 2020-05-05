from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.models import feedbackList
from datetime import datetime

class Feedback(Server):
    def __init__(self, request):
        super().__init__(request)
    
    def store_fb(self):
        intent = super().rcvIntent()
        first_name = super().rcvUserData('first_name')
        session = super().rcvSession()
        chat_ID = super().rcvUserData('id')
        rating = super().rcvParam('Rating')
        triggered_intent = super().rcvParam('triggered_intent')
        question = super().rcvParam('question')
        answer = super().rcvParam('answer')

        if rating == "👍":
            self.main_text = "Thank you for your input! ❤️"
            rating = 1
        elif rating == "👎":
            self.main_text = "I'm sorry you felt that way. If you wish to provide more comment, click here /feedback . We will look into this! ❤️"
            rating = 0
        else:
            self.main_text = "I don't understand. Please select thumbs up/down from the button! 😁"
            rating = -1
        
        if self.req.get('originalDetectIntentRequest').get('source') == "telegram":
            dict = {'intent' : intent,
                    'first_name' : first_name,
                    'session_ID' : session,
                    'chat_ID' : chat_ID,
                    'rating' : rating,
                    'triggered_intent' : triggered_intent,
                    'question' : question,
                    'answer' : answer,
                    }
            feedbackList.objects.create(**dict) #use ** to add dict into models

        return super().sendMsg(single=True)


    def store_text_fb(self):
        intent = super().rcvIntent()
        first_name = super().rcvUserData('first_name')
        session = super().rcvSession()
        chat_ID = super().rcvUserData('id')
        answer = super().rcvParam('feedback-comment')

        if self.req.get('originalDetectIntentRequest').get('source') == "telegram":
            dict = {'intent' : intent,
                    'first_name' : first_name,
                    'session_ID' : session,
                    'chat_ID' : chat_ID,
                    'rating' : -1,
                    'answer' : answer,
                    }
            feedbackList.objects.create(**dict) #use ** to add dict into models

        self.main_text = "Got'cha. Will definitely pass the message! 😜"
        return super().sendMsg(single=True)