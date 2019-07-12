import json
from key import key1
import numpy
from numpy import sys
from Matrix_Shaper import matrix_shaper
from key import key1


key = key1
Coords = ['25.680723,-100.365837']
with open('pedidos05_Julio_2019.json') as json_file:
    data = json.load(json_file)
    for p in data['records']:

        if p['datt_lat'] != '':
            Coords.append(p['datt_lat'] + ',' + p['datt_lon'])
            '''
            print('horario:' + p['horario'])
            '''
    # We insert the hub coordinates to the beginning.
    Coords.insert(0, "25.680723,-100.365837")
    print(Coords)
    row_count = int(len(Coords))
    # We count the max 10x10 squares we need for a row.
    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    increasing_counter = 0
    # This counter helps us to cut the number of requests roughly in half. This is due to the matrix being mirrored.
    destination_count = 0
    origin_count = 0
    # z counts the amount of requests being done. TODO: Possibly remove?
    z = 0
    origin_addresses = ""
    destination_addresses = ""
    matrix = numpy.zeros((row_count, row_count))
    print(matrix)

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
                    request = request + '&origins=' + origin_addresses + '&destinations=' + destination_addresses +\
                              '&key=' + key
                    print(i, q)
                    print(request)
                    matrix = matrix_shaper(matrix, i, q, request, destination_count, origin_count)
                    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
                    destination_addresses = ""
                    destination_count = 0
                    z = z + 1
            if destination_addresses != "":
                request = request + '&origins=' + origin_addresses + '&destinations=' + destination_addresses + '&key='\
                          + key
                print(i, q)
                print(request)
                matrix = matrix_shaper(matrix, i, q, request, destination_count, origin_count)
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
                request = request + '&origins=' + origin_addresses + '&destinations=' + destination_addresses + '&key='\
                          + key
                print(i, q)
                print(request)
                matrix = matrix_shaper(matrix, i, q, request, destination_count, origin_count)
                request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
                destination_addresses = ""
                destination_count = 0
                z = z + 1
        if destination_addresses != "":
            request = request + '&origins=' + origin_addresses + '&destinations=' + destination_addresses + '&key=' +\
                      key
            print(i, q)
            matrix = matrix_shaper(matrix, i, q, request, destination_count, origin_count)
            print(request)
            request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
            destination_addresses = ""
            destination_count = 0
            z = z + 1
        origin_count = 0
        origin_addresses = ""
        increasing_counter = increasing_counter + 10
    matrix = matrix.tolist()
    print(row_count)
    print(z)
    print(matrix)

