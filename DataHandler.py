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

# with open('pedidos05_Julio_2019.json') as json_file:
#    data = json.load(json_file)
# We insert the hub coordinates to the beginning.


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
#coord_dict = []
#pack = group_maker()
#coord_dict = clusterer(pack)

pack = {}
coord_dict = {1: [[25.7473953, -100.4032065], [25.7660635, -100.4637206], [25.6630098, -100.4530683], [25.6581939, -100.4584118], [25.6592963, -100.4465015], [25.7300825, -100.3996621], [25.7531641, -100.4408732], [25.7189575, -100.527637], [25.7574037, -100.4122195], [25.770444, -100.4339556]], 0: [[25.6694084, -100.3133837], [25.6412278, -100.2903594], [25.6621839, -100.2644861], [25.6706734, -100.3082421], [25.6413875, -100.3209291], [25.6677536, -100.307269], [25.6155781, -100.319466], [25.6078657, -100.26824], [25.691184, -100.2570771], [25.6658013, -100.3114536], [25.6661663, -100.3060847], [25.6394888, -100.2917929], [25.6411716, -100.2901994], [25.671679, -100.2839726], [25.6718855, -100.2474802], [25.6757692, -100.2920817], [25.6183025, -100.2728144], [25.5506444, -100.2336911]]}
key = key1
Coords = ['25.680723,-100.365837']

if coord_dict == []:
    user_input = input("Que horario? 1-> 8:00AM - 11:00AM, 2 -> 11:00AM - 2:00PM 3 -> 2:00PM - "
                       "5:00PM 4-> 5:00PM - 8:00PM")
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
                matrix_dict = data_handler(Coords)
else:
    x = 0
    matrix_dict = {}
    for w in coord_dict:
        matrix_dict.update({w: []})
        while x < len(coord_dict[w]):
            Coords.append(str(coord_dict[w][x][0]) + ',' + str(coord_dict[w][x][1]))
            x = x + 1
        matrix = data_handler(Coords)
        matrix_dict[w].append(matrix)
        Coords = ['25.680723,-100.365837']
    print(matrix_dict)

# for i in matrix_dict:
#    print(matrix_dict[i][0])

#create_data_model(matrix_dict)
#main()
