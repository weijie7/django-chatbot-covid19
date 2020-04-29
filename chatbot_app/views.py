from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

from chatbot_app.modules.features import Feature
from chatbot_app.models import feedbackList, userList, graphPlot
from chatbot_app.modules import multips

def index(request):
    image_obj = graphPlot.objects.order_by('name')
    image_dict = {'image_list' : image_obj}
    return render(request, r'chat_bot_template/index.html', image_dict)
    
    # image_list=[]
    # for root, dirs, files in os.walk(settings.STATIC_ROOT):
    #     for file in files:
    #         if file.endswith(".png"):
    #             image_list.append(file)
    # return render(request, r'chat_bot_template/index.html', context= {'imgs' : image_list})

@csrf_exempt
def webhook(request):
    # run Feature library
    print("Process ID for webhook: " + str(os.getpid()))
    feature = Feature(request)
    # start backend function
    return feature.main()
    # build a request object

def user_list(request):
    users = userList.objects.order_by('first_name')
    user_dict = {'table' : users}
    return render(request, r'chat_bot_template/user_list.html', user_dict)

def feedback_page(request):
    feedback_item = feedbackList.objects.order_by('datetime')
    feedback_dict = {'fb_table' : feedback_item}
    return render(request, r'chat_bot_template/feedback_page.html', feedback_dict)