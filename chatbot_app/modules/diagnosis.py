import pandas as pd
from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.models import diagnosisResponses

class Diagnosis(Server):
    def __init__(self, request):
        super().__init__(request)

    def diagnosis(self):
        try:
            # convert param value to boolean to process the conditions.
            param = ['Q1', 'Q2', 'S1', 'S2', 'S3']
            d = {}
            err = False

            for i, prm in enumerate(param):
                value_str = super().rcvParam(prm)
                print("value_str: "+ str(value_str))
                if value_str == "yes":
                    d[prm] = True
                elif value_str == "no":
                    d[prm] = False
                else:
                    raise "Invalid parameter value"
            print("decision dict: " + str(d))
            # decision dict: {'Q1': True, 'Q2': False....}

            # get diagnosis answer from django database
            res_list = list(diagnosisResponses.objects.values())

            # run the decision table with rule base system
            Q = int(d['Q1']) + int(d['Q2'])
            S = int(d['S1']) + int(d['S2']) + int(d['S3'])
            q1 = d['Q1']
            q2 = d['Q2']

            # High Risk 1
            if ((Q > 0) and (S > 0)) or ((Q==0) and (S==3)):
                self.main_text = res_list[0]['response'] 
            # High Risk 2
            elif q1 and (S==0):
                self.main_text = res_list[1]['response'] 
            # High Risk 3
            elif (not q1 and q2) and (S==0):
                self.main_text = res_list[2]['response'] 
            # Medium Risk 
            elif (Q==0) and (S==2):
                self.main_text = res_list[3]['response'] 
            # Low Risk 
            elif (Q==0) and (S==1):
                self.main_text = res_list[4]['response'] 
            # No Risk 
            elif (Q==0) and (S==0):
                self.main_text = res_list[5]['response'] 
            else:
                self.main_text = "Unknown response! Check for logics in Rule Base System."
        except "Invalid parameter value":
            self.main_text = "Parameter does not store either yes or no. Please check the entity naming in Dialogflow."
        finally:
            return super().sendMsg()


    def updateResponses(self):
        diagnosisResponses.objects.all().delete()

        #get data from excel file
        data = pd.read_excel('chatbot_app/components/database.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
        dlist = data["Responses"].tolist()
        res_list = [d.replace('\xa0',' ') for d in dlist]

        try:
            obj_list = [diagnosisResponses(response=text) for text in res_list]
            diagnosisResponses.objects.bulk_create(obj_list)
            print("Updated Diagnosis Responses.")
        except: 
            print("Error in uploading diagnosisResponses object to server. Check if objects are already exist.")
