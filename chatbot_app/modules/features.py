# apps modules
from chatbot_app.modules.status_news import StatusNews
from chatbot_app.modules.dist2hospital import Dist2Hospital
from chatbot_app.modules.diagnosis import Diagnosis
from chatbot_app.modules.webscrape import Webscrape
from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.modules.generate_graph import gen_graph
from chatbot_app.modules.feedback import feedback
from chatbot_app.modules.goodbye import goodbye
from chatbot_app.modules.subscription import subscribe
from chatbot_app.models import userList

#### FOR GLOBAL STATUS - FOR INFECTION STATUS INTENT ####

class Feature(Server):
    
    def __init__(self, request):
        self.sn = StatusNews(request)
        self.d2h = Dist2Hospital(request)
        self.dgs = Diagnosis(request)
        self.fb = feedback(request)
        self.gb = goodbye(request)
        self.sub = subscribe(request)
        self.wbs = Webscrape()
        self.gg = gen_graph()
        super().__init__(request)

        self.intent = super().rcvIntent()

        # --------------------------#
        # STORE USER INFO           #
        # --------------------------#
        first_name = super().rcvFirstName()
        chat_ID = super().rcvChatID()
        dict = {'first_name' : first_name,
                'chat_ID' : chat_ID
                }
        try:
            userList.objects.create(**dict) #use ** to add dict into models
            print('New user added.')
        except:
            print('User already exist. Skip')


    def main(self):
        # --------------------------#
        # INFECTION STATUS INTENT   #
        # --------------------------#
        if self.intent == "infection-status-covid":
            return self.sn.infectionStatus()

        # --------------------------#
        # HEADLINE NEWS INTENT      #
        # --------------------------#
        if self.intent == "latest-news-covid":
            return self.sn.headlineNews()

        # --------------------------#
        # Distance to Hospital      #
        # --------------------------#
        if self.intent == "nearest-hospital-covid" or self.intent == "treatment-covid.yes.address":
            return self.d2h.dist2hospital()

        # --------------------------#
        # DIAGNOSIS INTENT          #
        # --------------------------#
        if self.intent == "diagnosis-covid":
            return self.dgs.diagnosis()

        # --------------------------#
        # SYNC  INTENT              #
        # --------------------------#
        if self.intent == "sync":
            # try:
            self.wbs.statusScrapper()
            self.wbs.newsScrapper()
            self.dgs.updateResponses()
            self.gg.plot_it()
            self.main_text = "Sync/update completed."
            # except:
            #     self.main_text="Error occurred. Contact admin to debug."
            #     print("There is an error!")
            # finally:
            return super().sendMsg()

        # --------------------------#
        # FEEDBACK GATHER           #
        # --------------------------#
        if self.intent == "feedback-bad" or self.intent == "feedback-good":
            return self.fb.store_fb()
        
        # --------------------------#
        # GOODBYE                   #
        # --------------------------#
        if self.intent == "goodbye":
            return self.gb.bye()
        
        # --------------------------#
        # SUBSCRIPTION              #
        # --------------------------#
        if self.intent == "subscribe":
            return self.sub.sub()
        if self.intent == "unsubscribe":
            return self.sub.unsub()