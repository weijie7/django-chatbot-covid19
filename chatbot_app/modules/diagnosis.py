import sys
import pandas as pd
from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.models import diagnosisResponses
from chatbot_app.models import userDiagnosis

class Diagnosis(Server):
    def __init__(self, request):
        super().__init__(request)
        self.first_name = super().rcvUserData('first_name')
        self.chat_ID = super().rcvUserData('id')

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
                self.result = res_list[0]['query_ID']
                self.main_text = res_list[0]['response'] 
            # High Risk 2
            elif q1 and (S==0):
                self.result = res_list[1]['query_ID']
                self.main_text = res_list[1]['response'] 
            # High Risk 3
            elif (not q1 and q2) and (S==0):
                self.result = res_list[2]['query_ID']
                self.main_text = res_list[2]['response'] 
            # Medium Risk 
            elif (Q==0) and (S==2):
                self.result = res_list[3]['query_ID']
                self.main_text = res_list[3]['response'] 
            # Low Risk 
            elif (Q==0) and (S==1):
                self.result = res_list[4]['query_ID']
                self.main_text = res_list[4]['response'] 
            # No Risk 
            elif (Q==0) and (S==0):
                self.result = res_list[5]['query_ID']
                self.main_text = res_list[5]['response'] 
            else:
                self.main_text = "Unknown response! Check for logics in Rule Base System."
        except "Invalid parameter value":
            self.main_text = "Parameter does not store either yes or no. Please check the entity naming in Dialogflow."
        finally:
            # save diagnosis user data
            user_instant = userDiagnosis(first_name= self.first_name, chat_ID= self.chat_ID, diagnosis_result= self.result)
            try:
                user_instant.save()
                print('New user added for Diagnosis.')
            except Exception as e: 
                print('Error: '+str(e) + '. User already exists in Diagnosis. Overwrite diagnosis_result.')
                userDiagnosis.objects.filter(chat_ID=self.chat_ID).update(diagnosis_result= self.result)

            if self.result == 0:
                return super().sendMsg(get_fb=True, single=True)
            elif self.result == 1 or self.result == 2:
                return super().sendMsg(check_in=True, single=True)
            else:
                sys.exit("queryID is not 0, 1, or 2, Check excel file database.")

    def updateResponses(self):
        diagnosisResponses.objects.all().delete()

        #get data from excel file
        data = pd.read_excel('chatbot_app/components/database.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
        res_dict = data.to_dict('records')

        try:
            dgs_instance = [diagnosisResponses(response=d['Responses'].replace('\xa0',' '), query_ID=d['QueryID']) for d in res_dict]
            diagnosisResponses.objects.bulk_create(dgs_instance)
            print("Updated Diagnosis Responses.")
        except Exception as e: 
            print(e)
            print("Error in uploading diagnosisResponses object to server. Check if objects are already exist.")
