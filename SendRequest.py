# Sends a request to google's API, returning the time matrix of distances.
import requests
import time


def send_request(origin_addresses, dest_addresses, API_key):
    # Appends addresses to a single string, adding | in between.
    def build_address_str(addresses):
        address_str = ''
        for i in range(len(addresses)-1):
            address_str += addresses[i] + '|'
        address_str += addresses[-1]
        # Adds the last address. I'm not sure why it's needed, though. Seems weird.
        return address_str
    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    origin_address_str = build_address_str(origin_addresses)
    dest_address_str = build_address_str(dest_addresses)
    # Maximum 1000 elements per second. 10 requests per second.
    time.sleep(.1)
    request = request + '&origins=' + origin_address_str + '&destinations=' + dest_address_str + '&key=' + API_key
    response = requests.get(request)
    json_data = response.json()
    return json_data


