import os
import time
import geocoder
from geopy.geocoders import Nominatim
import json
# toronto scripts
full_path = os.path.realpath(__file__)
dpath, realfilename = os.path.split(full_path)

dpath +='/'



cityServices = {}
#cylce y/n
#circ, Lime ,Jump, LyftScooter, Bird, Skip, Spin, Voi, Tier, Wind ,Movo, Scoot
# n  , y    , y  , n          , n    , n ,   n   , n ,  n  ,  n  ,  n , n
cityServices['DC'] = ['Jump','Bird','LyftScooter','Lime','Skip','Spin']
cityServices['SanFrancisco'] = ['Scoot','Jump']
cityServices['TelAviv'] = ['Bird','Lime','Wind']
cityServices['MexicoCity'] = ['Lime','Movo']
cityServices['Brussels'] = ['Circ', 'Lime']
cityServices['Chicago'] = ['Jump','LyftScooter']
cityServices['Zurich'] = ['Tier','Bird']
cityServices['Detroit'] = ['Bird','Lime','Spin']
cityServices['Lisbon'] = ['Bird','Circ','Tier','Wind','Voi']
cityServices['Paris'] = ['Voi','Bird','Jump','Lime','Tier','Wind']
cityServices['Madrid'] = ['Voi','Bird','Jump','Circ','Lime','Tier','Wind']
import requests



URL = "https://geocode.search.hereapi.com/v1/geocode"
api_key = 'pErsqtJY_UMbH19rIvRyMlZc9KUzJeyTOCF6POWXHOQ' # Acquire from developer.here.com


universitiesGeolocations = {}

for city in cityServices:
    universitiesGeolocations[city] = {}
    fx = open(city+'.txt','r')
    content = fx.read()
    fx.close()
    geolocator = Nominatim(user_agent="scooterProject")
    content = content.split('\n')
    inst = 0
    for item in content:
        if item != '':
            if city == 'DC':
                item = item.split('\t')
                item = item[0]+ ' Washinton DC USA'

            elif city == 'SanFrancisco':
                if ',' in item:
                    item = item.split(',')
                    item = item[0]
                item = item+ ' San Francisco USA'

            elif city =='TelAviv':
                item = item.split('\t')
                item = item[0]+ ' Tel Aviv-Yafo'

            elif city =='MexicoCity':
                item = item.replace('Mexico City','')
                item = item.replace('...','')

                item = item.split('\t')
                loc = ''
                for i2 in item:
                    if len(i2) > len(loc):
                        loc = i2
                # item = loc+ ' '+city
                item = loc+ '  Mexico City'

            elif city =='Brussels' or city =='Chicago' or city =='Zurich' or city =='Detroit' or city =='Lisbon' or city =='Paris' or city == 'Madrid':
                item = item.replace('Brussels','')
                item = item.replace('...','')

                item = item.split('\t')
                loc = ''
                for i2 in item:
                    if len(i2) > len(loc):
                        loc = i2
                item = loc+ ' '+city


            # location = geolocator.geocode(item)
            PARAMS = {'apikey':api_key,'q':item}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()
            try:
                latitude = data['items'][0]['position']['lat']
                longitude = data['items'][0]['position']['lng']
                geoLoc = (latitude, longitude)
                print(inst,item, geoLoc)
                universitiesGeolocations[city][item] = geoLoc
                inst += 1
            except Exception as e:
                print('Exception!!',item)
                # time.sleep(10000)
    # time.sleep(10000)
    # break
fx = open('uniLocationsDict.txt','w')
fx.write(json.dumps(universitiesGeolocations))
fx.close()
