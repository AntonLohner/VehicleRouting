import numpy
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
    # z counts the amount of requests being done. Useful for making sure you're
    # not over requesting, same with the print() statements inside.
    z = 0
    origin_addresses = ""
    destination_addresses = ""
    matrix = numpy.zeros((row_count, row_count))
    print(matrix)
    # With N directions, we need to repeat N times a loop
    for i in range(row_count):
        if origin_addresses == "":
            origin_addresses = origin_addresses + coords[i]
        else:
            origin_addresses = origin_addresses + '|' + coords[i]
        origin_count = origin_count + 1

        # After appending 10 addresses, we need to append 10 destinations.
        if origin_count == 10:
            for q in range(row_count-increasing_counter):
                q = q + increasing_counter
                if destination_addresses == "":
                    destination_addresses = destination_addresses + coords[q]
                else:
                    destination_addresses = destination_addresses + '|' + coords[q]
                destination_count = destination_count + 1

                # Once we have 10 and 10, we send a request.
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
                # If the destination loop breaks, we need to make sure
                # that there aren't any final destinations to be sent in a request.
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
        # This is similar to the destination loop break checker, but for origins.
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
        # And once again checks that there aren't any final destinations to send.
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
# Sends a request to the enviaflores API to get a JSON response, returning the mty data.
pack = group_maker()
cluster_input = input("Are we making clusters? 1-> Yes. 2-> No ")
if cluster_input != "2":
    pause = "1"
    # Because clustering can give a wide variety of results, is relatively quick and doesn't cost anything,
    # I added a loop for testing.
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
            if 23 < float(pack[user_input][p]['latitude']) < 27 and -97 > \
                    float(pack[user_input][p]['longitude']) > -103:
                Coords.append((pack[user_input][p]['latitude'] + ',' + pack[user_input][p]['longitude']))
                print(Coords)
                # This isn't necessary, but I like being careful just in case. The print()s are also extra.
                if len(Coords) > 200:
                    closeit = input("Bigger than 200, please close :0")
        p = p + 1
    # We create a matrix_dict to have the output of this loop be similar to the cluster loop, making it easier to handle
    # either case later on.
    matrix_dict = {}
    matrix_dict.update({0: []})
    matrix = data_handler(Coords)
    matrix_dict[0].append(matrix)
else:
    x = 0
    # Makes a matrix dict and appends nodes:matrices to it.
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

# Same thing as the cluster loop, ORTools is relatively quick and doesn't cost anything. I've found it always gives the
# same results, though. The loop can probably be removed.
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