# apps modules
from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.modules.status_news import StatusNews
from chatbot_app.modules.dist2hospital import Dist2Hospital
from chatbot_app.modules.diagnosis import Diagnosis
from chatbot_app.modules.feedback import Feedback
from chatbot_app.modules.cbot_response import CbotResponse
from chatbot_app.modules.users_database import UserDB
from chatbot_app.modules.webscrape import Webscrape
from chatbot_app.modules.generate_graph import Gen_graph
from chatbot_app.modules.notification import Notification

#### FOR GLOBAL STATUS - FOR INFECTION STATUS INTENT ####

class Feature(Server):
    
    def __init__(self, request):
        super().__init__(request)
        self.sn = StatusNews(request)
        self.d2h = Dist2Hospital(request)
        self.dgs = Diagnosis(request)
        self.fb = Feedback(request)
        self.cr = CbotResponse(request)
        self.udb = UserDB(request)
        self.wbs = Webscrape()
        self.gg = Gen_graph()
        self.ntf = Notification()

        self.intent = super().rcvIntent()
        self.udb.storeId()

    def main(self):
        # --------------------------#
        # INFECTION STATUS INTENT   #
        # --------------------------#
        if self.intent == "infection-status-covid":
            return self.sn.infectionStatus()

        # --------------------------#
        # HEADLINE NEWS INTENT      #
        # --------------------------#
        elif self.intent == "latest-news-covid":
            return self.sn.headlineNews()

        # --------------------------#
        # Distance to Hospital      #
        # --------------------------#
        elif self.intent == "nearest-hospital-covid" or self.intent == "treatment-covid.yes.address":
            return self.d2h.dist2hospital()

        # --------------------------#
        # DIAGNOSIS INTENT          #
        # --------------------------#
        elif self.intent == "diagnosis-covid":
            return self.dgs.diagnosis()

        # --------------------------#
        # SYNC  INTENT              #
        # --------------------------#
        elif self.intent == "sync":
            # try:
            self.wbs.statusScrapper()
            self.wbs.newsScrapper()
            self.gg.plot_it()
            self.dgs.updateResponses()
            self.main_text = "Sync/update completed."
            # except:
            #     self.main_text="Error occurred. Contact admin to debug."
            #     print("There is an error!")
            # finally:
            return super().sendMsg(single=True)

        # --------------------------#
        # FEEDBACK GATHER           #
        # --------------------------#
        elif self.intent == "feedback-bad" or self.intent == "feedback-good":
            return self.fb.store_fb()

        # --------------------------#
        # FEEDBACK COMMENT          #
        # --------------------------#
        elif self.intent == "feedback":
            return self.fb.store_text_fb()
        
        # --------------------------#
        # GOODBYE                   #
        # --------------------------#
        elif self.intent == "goodbye":
            return self.cr.goodbye()
        
        # --------------------------#
        # SUBSCRIPTION              #
        # --------------------------#
        elif self.intent == "subscribe":
            return self.udb.subscribe()
        elif self.intent == "unsubscribe":
            return self.udb.unsubscribe()

        # --------------------------#
        # CHECKIN AFTER ASSESSMENT  #
        # --------------------------#
        elif self.intent == "checkin-yes" or self.intent == "checkin-no":
            return self.udb.checkin()

        # --------------------------#
        # CHECKIN NOTIFICATION      #
        # --------------------------#
        elif self.intent == "checkin-notification":
            self.ntf.send_checkin_days()
            self.main_text = "Notification sent!"
            return super().sendMsg(single=True)

