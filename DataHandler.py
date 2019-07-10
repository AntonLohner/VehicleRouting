import json
import math
import requests
from key import key1

key = ""
Coords = ['25.680723,-100.365837']
with open('pedidos05_Julio_2019.json') as json_file:
    data = json.load(json_file)
    for p in data['records']:
        print('horario:' + p['horario'])
        print('')
        if p['datt_lat'] != '':
            Coords.append(p['datt_lat'] + ',' + p['datt_lon'])
    # We insert the hub coordinates to the beginning.
    Coords.insert(0, "25.680723,-100.365837")
    print(Coords)
    row_count = int(len(Coords))
    # We count how many 10x10 squares we're going to make. (This is not the optimal solution, but it gets quite close
    # as our quantity of coords increases.
    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    increasing_counter = 0
    destination_count = 0
    origin_count = 0
    z = 0
    origin_addresses = ""
    destination_addresses = ""
    for i in range(row_count):
        if origin_addresses == "":
            origin_addresses = origin_addresses + Coords[i]
        else:
            origin_addresses = origin_addresses + '|' + Coords[i]
        origin_count = origin_count + 1
        if origin_count == 10:
            for q in range(row_count-increasing_counter):
                q = q + increasing_counter
                if destination_addresses == "":
                    destination_addresses = destination_addresses + Coords[q]
                else:
                    destination_addresses = destination_addresses + '|' + Coords[q]
                destination_count = destination_count + 1
                if destination_count == 10:
                    request = request + '&origins=' + origin_addresses + '&destinations=' + destination_addresses + '&key=' + key
                    print(i, q)
                    print(request)
                    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
                    destination_addresses = ""
                    destination_count = 0
                    z = z + 1
            if destination_addresses != "":
                request = request + '&origins=' + origin_addresses + '&destinations=' + destination_addresses + '&key=' + key
                print(i, q)
                print(request)
                request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
                destination_addresses = ""
                destination_count = 0
                z = z + 1
            origin_count = 0
            origin_addresses = ""
            increasing_counter = increasing_counter + 10
    if origin_addresses != "":
        for q in range(row_count-increasing_counter):
            q = q + increasing_counter
            if destination_addresses == "":
                destination_addresses = destination_addresses + Coords[q]
            else:
                destination_addresses = destination_addresses + '|' + Coords[q]
            destination_count = destination_count + 1
            if destination_count == 10:
                request = request + '&origins=' + origin_addresses + '&destinations=' + destination_addresses + '&key=' + key
                print(i, q)
                print(request)
                request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
                destination_addresses = ""
                destination_count = 0
                z = z + 1
        if destination_addresses != "":
            request = request + '&origins=' + origin_addresses + '&destinations=' + destination_addresses + '&key=' + key
            print(i, q)
            print(request)
            request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
            destination_addresses = ""
            destination_count = 0
            z = z + 1
        origin_count = 0
        origin_addresses = ""
        increasing_counter = increasing_counter + 10
    print(row_count)
    print(z)

