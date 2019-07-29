import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def basemap_plotter():
    # draws a merc map projection, a low resolution square limited by two of its corners- lower left and up right.
    map = Basemap(projection='merc', lat_0=25.4, lon_0=-100.3, resolution='l',
                  llcrnrlon=-100.6, llcrnrlat=25.5,
                  urcrnrlon=-100.1, urcrnrlat=25.9, epsg=3857
                  )
    # For other map options, see: http://server.arcgisonline.com/arcgis/rest/services

    return map


