from django.db import models

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
