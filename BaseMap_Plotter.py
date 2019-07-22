import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from test2 import A


def basemap_plotter(lons, lats):
    # draws a merc map projection, a high resolution square limited by two of its corners- lower left and up right.
    map = Basemap(projection='merc', lat_0=25.4, lon_0=-100.3, resolution='h',
                  llcrnrlon=-100.6, llcrnrlat=24.9,
                  urcrnrlon=-100.1, urcrnrlat=25.9, epsg=3857
                  )
    # For other map options, see: http://server.arcgisonline.com/arcgis/rest/services

    # draw coastlines, country/state boundaries, colour continents.
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    map.drawstates(linewidth=0.25)
    x, y = map(lons, lats)
    map.arcgisimage(service='World_Street_Map', xpixels=2500, verbose=True)
    map.plot(x, y, 'bo', markersize=2)

    plt.show()




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
