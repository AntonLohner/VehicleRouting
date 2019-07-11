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


def matrix_shaper(base_matrix, i, q, request):
    incremental_counter = 0
    time.sleep(.1)
    response = requests.get(request)
    json_data = response.json()
    for row in json_data['rows']:
        for j in range(len(json_data['destination_addresses'][:])):
            duration = [row['elements'][j]['duration']['value']]
            base_matrix[i-9+incremental_counter, q-9+j] = duration[0]
            base_matrix[q-9+j, i-9+incremental_counter] = duration[0]
            if base_matrix[i-9+incremental_counter, q-9+j] > -1:
                print("Replaced something that wasn't 0. Horizontal.")
            if base_matrix[q - 9 + j, i - 9 + incremental_counter] > -1:
                print("Replaced something that wasn't 0. Vertical.")
        incremental_counter = incremental_counter + 1
    return base_matrix
