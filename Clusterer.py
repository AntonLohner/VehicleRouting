import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
from sklearn.cluster import KMeans
from test2 import A
from BaseMap_Plotter import basemap_plotter
import math
lons = []
lats = []
centroid_lons = []
centroid_lats = []

#TODO: Remember the data will be split by hour.
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
# Currently, this more or less targets the coordinates that qualify inside Mty

df = pd.DataFrame({
    'x': lats,
    'y': lons
})
# Calculates the amount of clusters we want
k = math.ceil(len(lats)/20)
# Splits the data into the clusters
kmeans = KMeans(n_clusters=k, n_jobs=1)
# TODO: Optional due to google api restriction forcing us to overfit: Use elbow method to predict n_clusters
kmeans.fit(df)

labels = kmeans.predict(df)
centroids = kmeans.cluster_centers_

colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'y', 5: 'm', 6: 'c', 7: 'k', 8: 'w', 9: 'r', 10: 'g', 11: 'r', 12: 'g', 13: 'b',
          14: 'y', 15: 'm', 16: 'c', 17: 'k', 18: 'w', 19: 'r', 20: 'g', 21: 'g'}
fig = plt.figure(figsize=(5, 5))
colors = list(map(lambda x: colmap[x+1], labels))

# Cluster dictionary allows us to see if the clusters are too big or small
cluster_dict = {}
for i in range(0, int(k)):
    cluster_dict.update({i: 0})
for i in labels:
    cluster_dict[i] += 1
print(cluster_dict)

# We note which clusters we want to split and which ones we want to delete
splitter_list = []
target_list = []
for i in cluster_dict:
    if cluster_dict[i] < 5:
        print("Target acquired")
        print(i)
        target_list.append(i)
    if cluster_dict[i] > 30:
        print("Cluster too big")
        print(i)
        splitter_list.append(i)
labels = labels.tolist()
counter = 0

# Iterates through labels. The first for deletes the target clusters, while the second one splits the big ones into
# Clusters of hopefully 20-30. If a cluster was bigger than 50 we'd be in trouble, but we're handling data sets of
# about 100, so the odds of that are... pretty much 0. Something TODO: If time allows.

for i in labels:
    for x in target_list:
        if int(i) == x:
            del labels[counter]
            del lons[counter]
            del lats[counter]
            del colors[counter]
    y = 0
    while y < len(splitter_list):
        if int(i) == splitter_list[y]:
            if cluster_dict[int(i)] > 20:
                cluster_dict[y] = cluster_dict[y]-1
                labels[counter] = k+y
                # This allows you to visualize the splitting of nodes:
                colors[counter] = colmap[k+y+1]
        y = y + 1
    counter = counter + 1



# Sets the lat and long coordinates we're going to be looking at.
plt.ylim([-100.6, -100.1])
plt.xlim([25.5, 25.9])

basemap = basemap_plotter()

# Marks the centroid's latitudes and longitudes
for i in centroids:
    centroid_lons.append(float(i[0].item()))
    centroid_lats.append(float(i[1].item()))

# Plots the regular coordinates
x, y = basemap(lons, lats)
# Colors them depending on what cluster they're in
plt.scatter(x, y, color=colors, alpha=0.5, edgecolor='k')

# Plots the nodes
x, y = basemap(centroid_lats, centroid_lons)
i = 0
while i < math.ceil(len(lats)/20):
    plt.scatter(x[i], y[i], s=100, color=colmap[i+1], marker="v")
    i = i + 1

# Adds a fancy map background :0
basemap.arcgisimage(service='World_Street_Map', xpixels=2500, verbose=False)
# TODO: This is a really neat way to draw lines. Might be useful very soon. basemap.plot(x, y)
# TODO: Ask how aggressive we want to be in dropping the points that are very far away.
# TODO: Repeating the clustering 10x and dropping each time would work.

# The coord dictionary will help us know which nodes have which coordinates.
coord_dict = {}
for i in labels:
    coord_dict.update({i: []})
for i in range(0, len(lats)):
    coord_dict[labels[i]].append([lats[i], lons[i]])

# print(coord_dict)
plt.show()
