from django.db import models
from datetime import datetime
from chatbot_app.modules.storage import OverwriteStorage
import os

# Create your models here.

class globalStatus(models.Model):
    country = models.CharField(max_length=50, blank=False, unique=True)
    diagnosed = models.IntegerField()
    new_cases = models.IntegerField()
    death = models.IntegerField()
    new_death = models.IntegerField()
    discharged = models.IntegerField()
    active = models.IntegerField()
    critical = models.IntegerField()
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)

class globalLastUpdate(models.Model):
    last_update = models.CharField(max_length= 100)

class MOHHeadlines(models.Model):
    news_title = models.CharField(max_length=100, blank=False)
    news_link = models.URLField(unique = True)
    news_date = models.DateField(null=True)

class hospitalList(models.Model):
    hospital = 'HOSPITAL'
    polyclinic = 'POLYCLINIC'
    type_choice = [(hospital, 'Hospital'), (polyclinic, 'Polyclinic')]

    Name = models.CharField(max_length=100, blank=False, unique=True)
    Type = models.CharField(max_length=50, choices = type_choice, default= hospital)
    address = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()
    geocode_result = models.CharField(max_length = 5000)

class diagnosisResponses(models.Model):
    response = models.CharField(max_length=100, blank=False)
    query_ID = models.IntegerField()

class feedbackList(models.Model):
    intent = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=100, blank=True)
    telegram_user = models.CharField(max_length=100, blank=True)
    session_ID = models.CharField(max_length=100, blank=False)
    chat_ID = models.CharField(max_length=100)
    triggered_intent = models.CharField(max_length=100, blank=True)
    rating = models.IntegerField()
    question = models.CharField(max_length=10000)
    answer = models.CharField(max_length=10000)
    datetime = models.DateTimeField(auto_now = True)

class userList(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    telegram_user = models.CharField(max_length=100, blank=True)
    chat_ID = models.CharField(max_length=100,unique=True, blank=False)
    subscribe = models.BooleanField(default = True)
    
class graphPlot(models.Model):
    name = models.CharField(max_length=100, blank=False)
    plot = models.ImageField(upload_to ='plots/', storage=OverwriteStorage())
    datetime = models.DateTimeField(auto_now = True)

class userDiagnosis(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    chat_ID = models.CharField(max_length=100,unique=True, blank=False)
    datetime = models.DateTimeField(auto_now = True)
    diagnosis_result = models.CharField(max_length=1, blank=False)
    check_in = models.BooleanField(default = False)
