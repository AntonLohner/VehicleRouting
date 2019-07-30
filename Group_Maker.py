import json
import requests
from link import link
import datetime


def group_maker():
    # Sends a response, takes the json and returns only monterrey data from it.
    x = datetime.datetime.now()
    y = str(x)
    z = y[0:10]
    fecha = input("Que fecha deseas? Ej: 2019-07-12 No input -> Hoy ")
    if fecha != "":
        z = fecha
    example_link = str(link) + "date_from=" + z + "%2000:00:00&date_to=" + z + "%2023:59:59"
    response = requests.get(example_link)
    json_data = response.json()
    if json_data['result'] != "ok":
        print("Request result failed")
    # workshop_id = ["3", "396", "499", "678", "1133", "1168", "1966", "100874", "100954", "100955"]
    workshop_id = ["3"]
    hours = ["8:00AM - 11:00AM", "11:00AM - 2:00PM", "2:00PM - 5:00PM", "5:00PM - 8:00PM"]
    # roo_hours = ["1:00PM - 6:00PM", "8:00AM - 12:00AM", "12:00PM - 4:00PM","10:00AM - 3:00PM", "1:00PM - 6:00PM",
    #             "4:00PM - 7:00PM"]
    # Roo has all the weird hours.

    for i in workshop_id:
        for j in hours:
            try:
                print("Workshop: " + i)
                print("Hour: " + j)
                print(str(len(json_data["data"][z][i][j])) + " locations found")
            except KeyError:
                print("No data for this workshop and time.")
    package = json_data["data"][z]["3"]
    return package


