

def build_distance_matrix(response):
    distance_matrix = []
    print(response)
    for row in response['rows']:
        row_list = [row['elements'][j]['duration']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix
