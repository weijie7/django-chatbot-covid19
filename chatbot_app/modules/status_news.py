import pandas as pd
from datetime import datetime
from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.models import globalStatus, globalLastUpdate, MOHHeadlines
import random

class StatusNews(Server):
    def __init__(self, request):
        super().__init__(request)

    def infectionStatus(self):
        country = super().rcvParam('country-defined').lower()
        casestatus = super().rcvParam('CaseStatus')

        pd_table = pd.DataFrame(list(globalStatus.objects.all().values()))
        LastUpdate = list(globalLastUpdate.objects.all().values('last_update'))[0]['last_update']

        try:
            diagnose_ = pd_table[pd_table['country'] == country]['diagnosed'].iloc[0]
            death_ = pd_table[pd_table['country'] == country]['death'].iloc[0]
            discharged_ = pd_table[pd_table['country'] == country]['discharged'].iloc[0]
            active_ = pd_table[pd_table['country'] == country]['active'].iloc[0]
            critical_ = pd_table[pd_table['country'] == country]['critical'].iloc[0]
            new_case_ = pd_table[pd_table['country'] == country]['new_cases'].iloc[0]
            new_death_ = pd_table[pd_table['country'] == country]['new_death'].iloc[0]
          
        except:
            country = "worldwide"
            diagnose_ = pd_table['diagnosed'].sum()
            death_ = pd_table['death'].sum()
            discharged_ = pd_table['discharged'].sum()
            active_ = pd_table['active'].sum()
            critical_ = pd_table['critical'].sum()
            new_case_ = pd_table['new_cases'].sum()
            new_death_ = pd_table['new_death'].sum()

        #More info: https://github.com/Emmarex/dialogflow-fulfillment-python
        self.main_text = f'Currently, {country.capitalize()} has a total of {diagnose_:.0f} confirmed cases, + {new_case_:.0f} new case(s) from yesterday. There is total of {death_:.0f} death case(s), + {new_death_:.0f} new death case(s) from yesterday. \n\n{discharged_:.0f} people recovered from it, and {critical_:.0f} people still in critical condition. \n\n{LastUpdate}.'
        
        vkey = random.randrange(1,99999999,1)
        self.img_url = f"https://covid-chatbot.herokuapp.com/media/plots/{country}.png?v={vkey}"
        return super().sendMsg(get_fb=True, image=True)

    def headlineNews(self):
        news_list = list(MOHHeadlines.objects.order_by('-news_date').values())
        metatext = "Below are the top 3 latest news:\n"
        for news in news_list[:3]: #top3
            date_ = news['news_date'].strftime('%d %b, %Y')
            title_ = news['news_title']
            link_ = news['news_link']
            metatext = metatext + f"{date_} \n{title_} \n{link_}\n\n"
        
        self.main_text = metatext + "For more info: https://www.moh.gov.sg/covid-19"
        return super().sendMsg(get_fb=True, single=True)

