import googlemaps
from math import radians, sin, cos, acos
from datetime import datetime
from chatbot_app.modules.dialogflow_msg import Server
from chatbot_app.models import hospitalList
import os

class Dist2Hospital(Server):
    def __init__(self, request):
        super().__init__(request)
        self.__key = key_ = os.environ['key_']
        self.gmaps = googlemaps.Client(key = key_)

    def dist2hospital(self):
        address_ = super().rcvParam('address')
        
        try:
            premise_ = super().rcvParam('healthcare')
            if premise_ == '': 
                premise_ = 'Hospital'
            else:
                premise_ = premise_.capitalize()
        except:
            premise_ = 'Hospital'

        #for testing only. Pick 5th from hospital/clinic list
        premise_query = list(hospitalList.objects.filter(Type=premise_))
        #converting user-input starting point to geo-code lat & long
        geocode_result = self.gmaps.geocode(str(address_) + ' Singapore')

        if geocode_result==[]:
            self.text1 = 'Route not found. Perhaps check your address or postal code?'
        else:
            dist_list = [] 
            slat = radians(geocode_result[0]['geometry']['location']['lat'])
            slng = radians(geocode_result[0]['geometry']['location']['lng'])
            for item in premise_query:
                elat = radians(item.lat)
                elng = radians(item.lng)
                dist_list.append(6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slng - elng))) # this is original open list, for reference
            
            open_list = dist_list.copy()
            min_index = dist_list.index(min(dist_list)) #for search, find the min distance
            distance_result = self.gmaps.distance_matrix(str(address_) + ' Singapore', premise_query[min_index].address, departure_time=datetime.now())
            distance_gmap = distance_result['rows'][0]['elements'][0]['distance']['value']/1000 #convert m to km, this will be true distance
            duration_gmap = distance_result['rows'][0]['elements'][0]['duration']['value']/60 #convert sec to min
            solution = min_index #index of solution
            open_list.pop(min_index)
            print('original solution', premise_query[solution].Name, 'absolute distance is ', dist_list[solution], 'google final distance is ', distance_gmap)

            #check if open list has lesser distance than current one
            counter = 0
            while min(open_list) < distance_gmap:
                print('attempt', counter+1)
                new_min_index = dist_list.index(min(open_list))
                distance_result = self.gmaps.distance_matrix(str(address_) + ' Singapore', premise_query[new_min_index].address, departure_time=datetime.now())
                new_distance_gmap = distance_result['rows'][0]['elements'][0]['distance']['value']/1000
                new_duration_gmap = distance_result['rows'][0]['elements'][0]['duration']['value']/60 #convert sec to min
                open_list.remove(min(open_list))
                print('new solution', premise_query[new_min_index].Name, 'absolute distance is ', dist_list[new_min_index], 'google final distance is ', new_distance_gmap)
                if new_distance_gmap < distance_gmap:
                    solution = new_min_index #index of solution
                    distance_gmap = new_distance_gmap
                    duration_gmap = new_duration_gmap
                if open_list == []:
                    break
                counter+=1
                print('current solution', premise_query[solution].Name, 'absolute distance is ', dist_list[solution], 'google final distance is ', distance_gmap)

        self.main_text = f"Your location is {address_}, Singapore. Nearest {premise_} to you that I found is at {premise_query[solution].Name}. You are {distance_gmap:.1f}km away from it, it will take approximately {duration_gmap:.0f}min for you to reach there if you depart by car now."
        self.sub_text = f"Click link for instant direction: https://www.google.com/maps/dir/{str(address_.replace(' ','+'))+'+Singapore'}/{premise_query[solution].Name.replace(' ','+')}"
        return super().sendMsgs()
