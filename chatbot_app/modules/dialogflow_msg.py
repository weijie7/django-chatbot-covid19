# system modules
import sys
import json
from requests import get

# django module
from django import db
from django.http import HttpResponse, JsonResponse

# 3rd party library modules
from chatbot_app.modules.df_response_lib import *

class Server(object):
    def __init__(self, request):
        self.req = json.loads(request.body)
        self.main_text = None
        self.result = None
        self.sub_text = None
        self.img_url = None

    # get intent from dialogflow
    def rcvIntent(self):
        return self.req.get('queryResult').get('intent').get('displayName')

    # get parameter from dialogflow
    def rcvParam(self, key):
        return self.req.get('queryResult').get('parameters').get(key)

    # get session from dialogflow
    def rcvSession(self):
        return self.req.get('session').split('/')[-1]

    # get telegram data from dialogflow 
    def rcvUserData(self, key):
        if self.req.get('originalDetectIntentRequest').get('source') == "telegram":
            try:
                data = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('callback_query').get('from').get(key)
            except:
                data = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('from').get(key)
            if key == 'first_name':
                return data
            elif key == 'id':
                return str(data).split('.')[0]
        else:
            return None

    def sendMsg(self, get_fb=False, check_in=False, single=False, dual=False, image=False):
        #for single response only
        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text
        telegram = telegram_response()
        tel_main_text = telegram.text_response([self.main_text, self.main_text, False])

        if single == True:
            res_list = [tel_main_text]
            ans_list = [self.main_text]
        elif dual == True:
            tel_sub_text = telegram.text_response([self.sub_text, self.sub_text, False])
            res_list = [tel_main_text, tel_sub_text]
            ans_list = [self.main_text, self.sub_text]
        elif image == True:
            tel_img = telegram.image_response(self.img_url)
            res_list = [tel_main_text ,tel_img]
            ans_list = [self.main_text, self.img_url]
        else:
            sys.exit("Please set one of parameters (single, dual, image) as True!")

        #######Feedback#######
        if get_fb == True:
            #create feedback card response
            title = "How was I doing? Rate my response!"
            buttons = [
                ['👍','👍'],
                ['👎','👎']
            ]
            feedback_card = telegram.card_response(title, buttons)
            res_list.append(feedback_card)
            
            ff_add = ff_response.fulfillment_messages(res_list)

            #create context
            if single or dual or image:
                session = self.req.get('session')
                session_context = [
                                    ['feedback-followup', 1, {'question': self.req.get('queryResult').get('queryText') , 'answer': ans_list}]
                                ]
                #feedback-followup is input context for feedback. None for parameter
                output = ff_response.output_contexts(session, session_context)
        else:
            ff_add = ff_response.fulfillment_messages(res_list)
            output = None

        #######CheckIn#######
        if check_in == True:
            #create diagnosis card response
            if self.result == 1:
                title = "Seems like I can't be of certain that your symptoms is due to COVID-19. Would you want me to check in with you again after 2-3 days?"
            elif self.result == 2:
                title = "I can help to monitor your symptoms during your isolation period. Would you want me to check in with you after your isolation period?"
            else:
                sys.exit("queryID is not 0, 1, or 2, Check excel file database.")
            buttons = [
                ['Yes','👍'],
                ['No' ,'👎']
            ]
            feedback_card = telegram.card_response(title, buttons)
            res_list.append(feedback_card)
            
            ff_add = ff_response.fulfillment_messages(res_list)

            #create context
            session = self.req.get('session')
            session_context = [
                                ['checkin-followup', 1, {}]
                            ]
            #feedback-followup is input context for feedback. None for parameter
            output = ff_response.output_contexts(session, session_context)

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=output)
        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)
