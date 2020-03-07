from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pydialogflow_fulfillment import DialogflowResponse
from pydialogflow_fulfillment.response import SimpleResponse, OutputContexts
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from chatbot_app.models import globalStatus, globalLastUpdate, MOHHeadlines


# Create your views here.

def index(request):
    my_dict = {'variable': "Hello World"}
    return render(request, r'chat_bot_template/index.html', context= my_dict)

@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    # get action from json
    intent = req.get('queryResult').get('intent').get('displayName')

    # --------------------------#
    # INFECTION STATUS INTENT   #
    # --------------------------#
    if intent == "infection-status-covid":
        country = req.get('queryResult').get('parameters').get('country-defined')
        casestatus = req.get('queryResult').get('parameters').get('CaseStatus')

        pd_table = pd.DataFrame(list(globalStatus.objects.all().values()))
        LastUpdate = list(globalLastUpdate.objects.all().values('last_update'))[0]['last_update']

        try:
            diagnose_ = pd_table[pd_table['country'] == country]['diagnosed'].iloc[0]
            death_ = pd_table[pd_table['country'] == country]['death'].iloc[0]
            discharged_ = pd_table[pd_table['country'] == country]['discharged'].iloc[0]
            critical_ = pd_table[pd_table['country'] == country]['critical'].iloc[0]
            new_case_ = pd_table[pd_table['country'] == country]['new_cases'].iloc[0]
            new_death_ = pd_table[pd_table['country'] == country]['new_death'].iloc[0]
            
        except:
            country = "Worldwide"
            diagnose_ = pd_table['diagnosed'].sum()
            death_ = pd_table['death'].sum()
            discharged_ = pd_table['discharged'].sum()
            critical_ = pd_table['critical'].sum()
            new_case_ = pd_table['new_cases'].sum()
            new_death_ = pd_table['new_death'].sum()

        #More info: https://github.com/Emmarex/dialogflow-fulfillment-python
        text1 = f'Currently, {country.capitalize()} has a total of {diagnose_:.0f} confirmed cases, + {new_case_:.0f} new case(s) from yesterday. There is total of {death_:.0f} death case(s), + {new_death_:.0f} new death case(s) from yesterday. \n\n{discharged_:.0f} people recovered from it, and {critical_:.0f} people still in critical condition. \n\n{LastUpdate}.'
   
    # --------------------------#
    # HEADLINE NEWS INTENT      #
    # --------------------------#
    if intent == "latest-news-covid":
        news_list = list(MOHHeadlines.objects.order_by('news_date').values())
        for news in news_list[-3:]: #top3
            date_ = news['news_date'].strftime('%d %b, %Y')
            title_ = news['news_title']
            link_ = news['news_link']
            text1 = f"{date_} \n{title_} \n{link_}\n\nFor more info: https://www.moh.gov.sg/covid-19"


    dialogflow_response = DialogflowResponse(text1)
    reply = dialogflow_response.get_final_response()

    # return generated response
    return HttpResponse(reply, content_type='application/json; charset=utf-8')

