import json
import requests
import link
import datetime
from Test import example_return
x = datetime.datetime.now()
y = str(x)
z = y[0:10]

example_return = example_return
example_link = str(link) + "date_from=" + z + "%2000:00:00&date_to=" + z + "%2023:59:59"
#response = requests.get(example_link)
#json_data = response.json()
#if json_data['result'] != "ok":
#    print("Request result failed")
#print(json_data)


workshop_id = ["3", "396", "499", "678", "1133", "1168", "1966", "100874", "100954", "100955"]
hours = ["8:00AM - 11:00AM", "11:00AM - 2:00PM", "2:00PM - 5:00PM", "5:00PM - 8:00PM"]
roo_hours = ["1:00PM - 6:00PM", "8:00AM - 12:00AM", "12:00PM - 4:00PM","10:00AM - 3:00PM", "1:00PM - 6:00PM", "4:00PM - 7:00PM"]

# Roo has all the weird hours.
for i in workshop_id:
    for j in hours:
        try:
            print("Workshop: " + i)
            print("Hour: " + j)
            print(str(len(example_return["data"]["2019-07-12"][i][j])) + " locations found")
        except KeyError:
            print("No data for this workshop and time.")

print(len(example_return["data"]["2019-07-12"]["3"]["8:00AM - 11:00AM"]))
print(len(example_return["data"]["2019-07-12"]["100955"]))
print(example_return["data"]["2019-07-12"]["100955"]["8:00AM - 11:00AM"])
# TODO: Add a warning if there's too many customers in a zone, which would cause an increase in google api costs.
# TODO: Ideally we want lists of maximum 100? 100^2/200 = 50*16 = 800 requests = 400 dollars? 50 max -> 200 dollars?
# TODO: Only for the general sorting, which we'll compare to a couple more subtle approaches.


# TODO: Ask for the Json to be updated to include Lat/Long
