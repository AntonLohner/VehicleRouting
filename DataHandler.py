import json
from key import key1
import numpy
from numpy import sys
from Matrix_Shaper import matrix_shaper
from key import key1
from Clusterer import clusterer
from Group_Maker import group_maker
from TimeMartixProcessing import main
from CreateDataModel import create_data_model


def data_handler(coords):
    row_count = int(len(coords))
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
            origin_addresses = origin_addresses + coords[i]
        else:
            origin_addresses = origin_addresses + '|' + coords[i]
        origin_count = origin_count + 1
        if origin_count == 10:
            for q in range(row_count-increasing_counter):
                q = q + increasing_counter
                if destination_addresses == "":
                    destination_addresses = destination_addresses + coords[q]
                else:
                    destination_addresses = destination_addresses + '|' + coords[q]
                destination_count = destination_count + 1
                if destination_count == 10:
                    request = request + '&origins=' + origin_addresses + '&destinations=' + destination_addresses +\
                              '&key=' + key
                    print(i, q)
                    print(request)
                    matrix = matrix_shaper(matrix, i, q, request, destination_count, origin_count)
                    print(matrix)
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
                print(matrix)
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
                destination_addresses = destination_addresses + coords[q]
            else:
                destination_addresses = destination_addresses + '|' + coords[q]
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
    return matrix

######################
coord_dict = []
pack = group_maker()
cluster_input = input("Are we making clusters? 1-> Yes. 2-> No ")
if cluster_input != "2":
    pause = "1"
    while pause == "1":
        coord_dict = clusterer(pack)
        pause = input("Redo? 1 = yes")
key = key1
Coords = ['25.680723,-100.365837']

if coord_dict == []:
    user_input = input("Que horario? 1-> 8:00AM - 11:00AM, 2 -> 11:00AM - 2:00PM 3 -> 2:00PM - "
                       "5:00PM 4-> 5:00PM - 8:00PM ")
    if user_input == "1":
        user_input = "8:00AM - 11:00AM"
    if user_input == "2":
        user_input = "11:00AM - 2:00PM"
    if user_input == "3":
        user_input = "2:00PM - 5:00PM"
    if user_input == "4":
        user_input = "5:00PM - 8:00PM"
    p = 0
    while p < len(pack[user_input]):
        if pack[user_input][p]['latitude'] == "":
            ""
        else:
            # TODO: Consider if this is necessary nowadays.
            if 23 < float(pack[user_input][p]['latitude']) < 27 and -97 > \
                    float(pack[user_input][p]['longitude']) > -103:
                Coords.append((pack[user_input][p]['latitude'] + ',' + pack[user_input][p]['longitude']))
                print(Coords)
                if len(Coords) > 200:
                    closeit = input("Bigger than 200, please close :0")
        p = p + 1
    matrix_dict = {}
    matrix_dict.update({0: []})
    closeit = input("Please double check.")
    matrix = data_handler(Coords)
    matrix_dict[0].append(matrix)
    print(matrix_dict)
else:
    x = 0
    matrix_dict = {}
    for w in coord_dict:
        matrix_dict.update({w: []})
        while x < len(coord_dict[w]):
            Coords.append(str(coord_dict[w][x][0]) + ',' + str(coord_dict[w][x][1]))
            x = x + 1
        print(Coords)
        matrix = data_handler(Coords)
        matrix_dict[w].append(matrix)
        Coords = ['25.680723,-100.365837']
        x = 0
    print(matrix_dict)
redo = "y"
while redo == "y":
    for i in matrix_dict:
        total_num_vehicles = 6
        model_matrix = matrix_dict[i][0]
        if coord_dict == []:
            data_model = create_data_model(model_matrix, total_num_vehicles)
            main(data_model, Coords)
        else:
            total_num_vehicles = 1
            data_model = create_data_model(model_matrix, total_num_vehicles)
            main(data_model, coord_dict[i])
    redo = input("Do you want to retry the OR Solution? y = yes ")
    i = 0

    # matrix_dict

# for i in matrix_dict:
#    print(matrix_dict[i][0])

#create_data_model(matrix_dict)
#main()