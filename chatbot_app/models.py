from django.db import models

# Create your models here.

class globalStatus(models.Model):
    country = models.CharField(max_length=50, blank=False, unique=True)
    diagnosed = models.IntegerField()
    new_cases = models.IntegerField()
    death = models.IntegerField()
    new_death = models.IntegerField()
    discharged = models.IntegerField()
    critical = models.IntegerField()
    region = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)

class globalLastUpdate(models.Model):
    last_update = models.CharField(max_length= 100)

class MOHHeadlines(models.Model):
    news_title = models.CharField(max_length=100, blank=False)
    news_link = models.URLField(unique = True)
    news_date = models.DateField(null=True)
