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

    def rcvIntent(self):
        return self.req.get('queryResult').get('intent').get('displayName')

    def rcvParam(self, value):
        return self.req.get('queryResult').get('parameters').get(value)

    def sendMsg(self):
        #for single response only
        telegram = telegram_response()

        ff_response = fulfillment_response() #create class
        ff_text = ff_response.fulfillment_text(self.main_text) #insert ff text as first response, text only hence use fulfillment_text
        reply = ff_response.main_response(ff_text)

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
        ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_sub_text])
        reply = ff_response.main_response(ff_text, ff_add)

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
        ff_add = ff_response.fulfillment_messages([tel_main_text ,tel_img])
        reply = ff_response.main_response(ff_text, ff_add)

        db.connections.close_all()
        # return generated response
        return JsonResponse(reply, safe=False)