import numpy as np
import requests
import time

'''
matrix = np.zeros((20, 20))
matrix2 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
print(matrix)
print(matrix2)
incremental_counter = 0
for x in range(10):
    for j in range(10):
        j = j
        duration = matrix2[j]
        matrix[9-9+incremental_counter, 19-9+j] = duration
        matrix[19 - 9 + j, 9 - 9 + incremental_counter] = duration
    incremental_counter = incremental_counter + 1
print(matrix)
print(type(matrix))
'''


def matrix_shaper(base_matrix, i, q, request, destination_count, origin_count):
    x = 1
    incremental_counter = 0
    time.sleep(.1/4)
    # TODO: The sleep time can go lower or higher depending on how long the code takes to execute.
    response = requests.get(request)
    json_data = response.json()
    for row in json_data['rows']:
        for j in range(len(json_data['destination_addresses'][:])):
            duration = [row['elements'][j]['duration']['value']]
            while json_data['rows'][0]['elements'][0]['status'][:] != 'OK':
                print("Status is not OK:", i, q)
                time.sleep(2**x)
                response = requests.get(request)
                json_data = response.json()
                x = x + 1
                if x == 5:
                    break
            base_matrix[i-origin_count+incremental_counter, q-destination_count+j] = duration[0]
            base_matrix[q-destination_count+j, i-origin_count+incremental_counter] = duration[0]
        incremental_counter = incremental_counter + 1
    return base_matrix
