from django.contrib import admin

# Register your models here.
from chatbot_app.models import globalStatus, globalLastUpdate, MOHHeadlines, hospitalList
admin.site.register(globalStatus)
admin.site.register(globalLastUpdate)
admin.site.register(MOHHeadlines)
admin.site.register(hospitalList)