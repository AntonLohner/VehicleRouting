import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def basemap_plotter():
    # draws a merc map projection, a high resolution square limited by two of its corners- lower left and up right.
    map = Basemap(projection='merc', lat_0=25.4, lon_0=-100.3, resolution='l',
                  llcrnrlon=-100.6, llcrnrlat=25.5,
                  urcrnrlon=-100.1, urcrnrlat=25.9, epsg=3857
                  )
    # For other map options, see: http://server.arcgisonline.com/arcgis/rest/services

    # draw coastlines, country/state boundaries, colour continents.
#    map.drawcoastlines(linewidth=0.25)
#    map.drawcountries(linewidth=0.25)
#    map.drawstates(linewidth=0.25)

    return map



#lons = []
#lats = []
#for i in A["records"]:
#    if i['datt_lon'] == "":
#        ""
#    else:
#        if float(i['datt_lat']) > 23:
#            if float(i['datt_lat']) < 27:
#                if float(i['datt_lon']) < -97:
#                    if float(i['datt_lon']) > -103:
#                        lons.append(float(i['datt_lon']))
#                        lats.append(float(i['datt_lat']))
#print(lons)
#print(lats)
#basemap_plotter(lons, lats)
