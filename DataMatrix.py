import math
from SendRequest import send_request
from MatrixBuilder import build_distance_matrix


def create_distance_matrix(data):
    key = "AIzaSyATq8bhhn73jqukR0xqpRcWafNLeldMoYo"
    # TODO: REPLACE THE KEY

    # We have a maximum of 100 elements per request, so we're splitting the rows to fit that restriction
    # TODO: When data is replaced, this will change
    addresses = data
    num_addresses = len(addresses)
    max_rows = int(math.floor(100./num_addresses))
    # q = number of full rows, while r = the remainder
    q, r = divmod(num_addresses, max_rows)
    q = int(q)
    distance_matrix = []

    for i in range(q):
        origin_addresses = data[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, data, key)
        distance_matrix += build_distance_matrix(response)

    if r > 0:
        origin_addresses = data[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, data, key)
        distance_matrix += build_distance_matrix(response)
    return distance_matrix





