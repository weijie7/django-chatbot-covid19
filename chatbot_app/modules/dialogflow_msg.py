# system modules
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
        self.sub_text = None
        self.img_url = None
        self.get_input = None
        self.first_name = None

    def rcvIntent(self):
        return self.req.get('queryResult').get('intent').get('displayName')

    def rcvParam(self, value):
        return self.req.get('queryResult').get('parameters').get(value)

    def rcvFirstName(self):
        if self.req.get('originalDetectIntentRequest').get('source') == "telegram":
            try:
                fn = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('callback_query').get('from').get('first_name')
            except:
                fn = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('from').get('first_name')
            return fn
        else:
            return None

    def rcvChatID(self):
        if self.req.get('originalDetectIntentRequest').get('source') == "telegram":
            try:
                id_ = self.req.get   ('originalDetectIntentRequest').get('payload').get('data').get('callback_query').get('from').get('id')
            except:
                id_ = self.req.get('originalDetectIntentRequest').get('payload').get('data').get('from').get('id')
            return str(id_).split('.')[0]
        else:
            return None

    def sendMsg(self):
        #for single response only
        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text
        telegram = telegram_response()
        tel_main_text = telegram.text_response([self.main_text, self.main_text, False])

        #######Feedback#######
        if self.get_input == 1:
            #create feedback card response
            title = "How was I doing? Rate my response!"
            buttons = [
                ['👍','👍'],
                ['👎','👎']
            ]
            feedback_card = telegram.card_response(title, buttons)
            ff_add = ff_response.fulfillment_messages([tel_main_text ,feedback_card])

            #create context
            session = self.req.get('session')
            session_context = [
                                    ['feedback-followup', 1, {'question': self.req.get('queryResult').get('queryText') , 'answer': [self.main_text]}]
                                ]
            #feedback-followup is input context for feedback. None for parameter
            output = ff_response.output_contexts(session, session_context)
        else:
            ff_add = None
            output = None

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=output)
        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)


    def sendMsgs(self):
        #for dual response
        telegram = telegram_response()
        tel_main_text = telegram.text_response([self.main_text, self.main_text, False])
        tel_sub_text = telegram.text_response([self.sub_text, self.sub_text, False])

        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text

        #######Feedback#######
        if self.get_input == 1:
            #create feedback card response
            title = "How was I doing? Rate my response!"
            buttons = [
                ['👍','👍'],
                ['👎','👎']
            ]
            feedback_card = telegram.card_response(title, buttons)
            ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_sub_text, feedback_card])

            #create context
            session = self.req.get('session')
            session_context = [
                                    ['feedback-followup', 1, {'question': self.req.get('queryResult').get('queryText') , 'answer': [self.main_text, self.sub_text]}]
                                ]
            #feedback-followup is input context for feedback. None for parameter
            output = ff_response.output_contexts(session, session_context)
        else:
            ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_sub_text])
            output = None

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=output)

        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)

    def sendMsgImg(self):
        #for msg + img response
        telegram = telegram_response()
        tel_main_text = telegram.text_response([self.main_text, self.main_text, False])
        tel_img = telegram.image_response(self.img_url)

        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text

        #######Feedback#######
        if self.get_input == 1:
            #create feedback card response
            title = "How was I doing? Rate my response!"
            buttons = [
                ['👍','👍'],
                ['👎','👎']
            ]
            feedback_card = telegram.card_response(title, buttons)
            ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_img, feedback_card])

            #create context
            session = self.req.get('session')
            session_context = [
                                    ['feedback-followup', 1, {'question': self.req.get('queryResult').get('queryText') , 'answer': [self.main_text, self.img_url]}]
                                ]
            #feedback-followup is input context for feedback. None for parameter
            output = ff_response.output_contexts(session, session_context)
        else:
            ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_img])
            output = None

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=output)

        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)


    def feedbackMsg(self):
        #for feedback response only
        ff_response = fulfillment_response() #create class
        telegram = telegram_response()

        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text
        feedback_card = telegram.card_response(self.main_text, None)
        ff_add = ff_response.fulfillment_messages([feedback_card])

        reply = ff_response.main_response(fulfillment_text=ff_text, fulfillment_messages = ff_add, output_contexts=None)
        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)