import requests
import time
import json
from link import link

def city_placer(lat, long):
    request = "link.format(str(long), str(lat))
    response = requests.get(request)
    json_data = response.json()
    x = 1
    while json_data['result'] != "ok":
        response = requests.get(request)
        json_data = response.json()
        x = x + 1
        if x == 2:
            json_data = {'result': 'ok', 'data': {'store_slug': ''}}
    return json_data['data']['store_slug']


CityList = []
with open('pedidos05_Julio_2019_backup.json') as json_file:
    data = json.load(json_file)
    for p in data['records']:
        if p['datt_lat'] != '':
            Lat = p['datt_lat']
            Long = p['datt_lon']
            CityList.append(city_placer(Lat, Long))
print(CityList)

