from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

from chatbot_app.modules.features import Feature
#key_ = os.environ['AIzaSyCpqFU-7MTe4GSgFzuobfscIYm1E-tLrgY']
#gmaps = googlemaps.Client(key = key_)


# Create your views here.

def index(request):
    image_list=[]
    for root, dirs, files in os.walk(settings.STATIC_ROOT):
        for file in files:
            if file.endswith(".png"):
                image_list.append(file)
    return render(request, r'chat_bot_template/index.html', context= {'imgs' : image_list})


@csrf_exempt
def webhook(request):
    # run Feature library
    feature = Feature(request)
    # start backend function
    return feature.main()
    # build a request object
