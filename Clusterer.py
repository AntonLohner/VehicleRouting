import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
from sklearn.cluster import KMeans
from test2 import A
from BaseMap_Plotter import basemap_plotter

lons = []
lats = []
for i in A["records"]:
    if i['datt_lon'] == "":
        ""
    else:
        if float(i['datt_lat']) > 23:
            if float(i['datt_lat']) < 27:
                if float(i['datt_lon']) < -97:
                    if float(i['datt_lon']) > -103:
                        lons.append(float(i['datt_lon']))
                        lats.append(float(i['datt_lat']))
# Set the problem. Add the target coordinates. These will be lats/longs, I assume.

df = pd.DataFrame({
    'x': lats,
    'y': lons
})

kmeans = KMeans(n_clusters=3, n_jobs=1)
# TODO: Use elbow method to predict n_clusters
kmeans.fit(df)

labels = kmeans.predict(df)
centroids = kmeans.cluster_centers_

colmap = {1: 'r', 2: 'g', 3: 'b'}
fig = plt.figure(figsize=(5, 5))
colors = list(map(lambda x: colmap[x+1], labels))
plt.scatter(df['x'], df['y'], color=colors, alpha=0.5, edgecolor='k')
for idx, centroid in enumerate(centroids):
    plt.scatter(*centroid, color=colmap[idx+1])


plt.ylim([-100.6, -100.1])
plt.xlim([24.9, 25.9])
plt.show()


basemap_plotter(lons, lats)