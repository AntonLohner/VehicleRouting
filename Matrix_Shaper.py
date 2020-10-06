import numpy as np
import requests
import time

# Because the google OR tool required a distance matrix, and google maps had a limit of 100 points per request, i'd make distance matrixes and stich them 
# to make the complete matrix, which would then be solved by OR tools.
def matrix_shaper(base_matrix, i, q, request, destination_count, origin_count):
    x = 1
    incremental_counter = 0
    time.sleep(.1/4)
    response = requests.get(request)
    json_data = response.json()
    # Sends a response, limited by the google API's requests per second limit.
    for row in json_data['rows']:
        for j in range(len(json_data['destination_addresses'][:])):
            duration = [row['elements'][j]['duration']['value']]
            while json_data['rows'][0]['elements'][0]['status'][:] != 'OK':
                print("Status is not OK:", i, q)
                # If there's an error, delays the next request.
                time.sleep(2**x)
                response = requests.get(request)
                json_data = response.json()
                x = x + 1
                if x == 5:
                    break
            # Adds the 10 by 10 matrix into the square it goes in, and then does the same for it's "mirror reflection"
            base_matrix[i-origin_count+incremental_counter, q-destination_count+j] = duration[0]
            base_matrix[q-destination_count+j, i-origin_count+incremental_counter] = duration[0]
        incremental_counter = incremental_counter + 1
    return base_matrix
