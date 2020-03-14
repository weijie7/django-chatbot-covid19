import sys
import django
import os
os.environ.setdefault('DJANGO_SETTING_MODULE', 'ChatBot_Main.settings')
# setting can be found in wsgi.py folder in pycache
os.environ['DJANGO_SETTINGS_MODULE'] = 'ChatBot_Main.settings'
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from chatbot_app.models import globalStatus, globalLastUpdate, MOHHeadlines, hospitalList
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import googlemaps
import json


#gmaps = googlemaps.Client(key = 'AIzaSyCpqFU-7MTe4GSgFzuobfscIYm1E-tLrgY')

df = pd.read_csv(r'hospital & polyclinic.csv')
df['address'] = None
df['lat'] = None
df['lng'] = None
df['geocode_result'] = None

def populate_hospital(df):
    for i in range(len(df)):
        geocode_result = gmaps.geocode(df['Name'][i] + " Singapore") 
        df['geocode_result'][i] = json.dumps(geocode_result)
        df['address'][i] = geocode_result[0]['formatted_address']
        df['lat'][i] = geocode_result[0]['geometry']['location']['lat']
        df['lng'][i] = geocode_result[0]['geometry']['location']['lng']

populate_hospital(df)
hospital_dict = df.to_dict('records')
model_instance = [hospitalList(Name=i['Name'], Type=i['Type'], address=i['address'], lat=i['lat'], lng=i['lng'], geocode_result=i['geocode_result']) for i in hospital_dict]

hospitalList.objects.bulk_create(model_instance)
print('Update success')