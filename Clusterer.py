import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
from sklearn.cluster import KMeans
# from test2 import A
from BaseMap_Plotter import basemap_plotter
import math
import sys


def clusterer(input_data):
    lons = []
    lats = []
    centroid_lons = []
    centroid_lats = []

    user_input = input("Que horario? 1-> 8:00AM - 11:00AM, 2 -> 11:00AM - 2:00PM 3 -> 2:00PM - "
                       "5:00PM 4-> 5:00PM - 8:00PM ")
    if user_input == "1":
        user_input = "8:00AM - 11:00AM"
    if user_input == "2":
        user_input = "11:00AM - 2:00PM"
    if user_input == "3":
        user_input = "2:00PM - 5:00PM"
    if user_input == "4":
        user_input = "5:00PM - 8:00PM"
    i = 0
    while i < len(input_data[user_input]):
        if input_data[user_input][i]['latitude'] == "":
            ""
        else:
            # TODO: Consider if this is necessary nowadays.
            if 23 < float(input_data[user_input][i]['latitude']) < 27 and -97 > \
                    float(input_data[user_input][i]['longitude']) > -103:
                lats.append(float(input_data[user_input][i]['latitude']))
                lons.append(float(input_data[user_input][i]['longitude']))
        i = i + 1
    # Set the problem. Add the target coordinates. These will be lats/longs, I assume.
    # Currently, this more or less targets the coordinates that qualify inside Mty
    df = pd.DataFrame({
        'x': lats,
        'y': lons
    })
    # Calculates the amount of clusters we want
    num_clusters = input("How many clusters? Ex: 5 ")
    num_clusters = int(num_clusters)
    #num_clusters = math.ceil(len(lats)/20)
    # Splits the data into the clusters
    kmeans = KMeans(n_clusters=num_clusters, n_jobs=1)
    # TODO: Optional due to google api restriction forcing us to overfit: Use elbow method to predict n_clusters
    kmeans.fit(df)

    labels = kmeans.predict(df)
    centroids = kmeans.cluster_centers_
    colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'y', 5: 'm', 6: 'c', 7: 'k', 8: 'w', 9: 'r', 10: 'g', 11: 'b', 12: 'y', 13: 'm',
              14: 'c', 15: 'k', 16: 'w', 17: 'r', 18: 'g', 19: 'b', 20: 'y', 21: 'm'}
    fig = plt.figure(figsize=(5, 5))

    # Cluster dictionary allows us to see if the clusters are too big or small
    cluster_dict = {}
    for i in range(0, int(num_clusters)):
        cluster_dict.update({i: 0})
    for i in labels:
        cluster_dict[i] += 1
    for i in cluster_dict:
        if cluster_dict[i] > 50:
            user_input = input("Warning, there's a 50+ cluster. This would result in a probable 30+ distance matrix. "
                               "Are you sure you want to continue? Y or N ")
            if user_input != "Y":
                sys.exit("Program stopped by user.")

    # We note which clusters we want to split and which ones we want to delete
    splitter_list = []
    target_list = []
    print(cluster_dict)
    for i in cluster_dict:
        if cluster_dict[i] < 5:
            print("Cluster too small")
            print(i)
            target_list.append(i)
        if cluster_dict[i] > 30:
            #print("Cluster too big")
            #print(i)
            splitter_list.append(i)
    labels = labels.tolist()
    counter = 0

    # Iterates through labels. The first for deletes the target clusters, while the second one splits the big ones into
    # Clusters of hopefully 20-30. If a cluster was bigger than 50 we'd be in trouble, but we're handling data sets of
    # about 100, so the odds of that are... pretty much 0. Something TODO: If time allows.
    big_node_lats = []
    big_node_lons = []

    centroids = centroids.tolist()
    global_list = splitter_list + target_list
    global_list.sort()
    i = len(global_list)
    while i > 0:
        del centroids[global_list[i-1]]
        i = i - 1

    while i < len(labels):
        for x in target_list:
            if labels[i] == x:
                #print("delet this")
                # TODO: Note the fallen
                del labels[i]
                del lons[i]
                del lats[i]
                i = i - 1
        for y in splitter_list:
            if labels[i] == y:
                #print("The bigger they are, the harder they fall.")
                big_node_lons.append(lons[i])
                big_node_lats.append(lats[i])
                # This is the part where we do stuff
                del labels[i]
                del lons[i]
                del lats[i]
                i = i - 1
        counter = counter + 1
        i = i + 1

    # We create two clusters out of the big clusters, in order to reduce the number of addresses required in the google API.
    # TODO: If we have the time, i'd like to just have it iterate infinitely as long as it doesn't create clusters that are
    # TODO: small enough.
    df2 = pd.DataFrame({
        'x': big_node_lats,
        'y': big_node_lons
    })

    colors = list(map(lambda x: colmap[x+1], labels))
    if len(big_node_lons) > 2:
        kmeans2 = KMeans(n_clusters=len(splitter_list)*2, n_jobs=1)
        kmeans2.fit(df2)
        labels2 = kmeans2.predict(df2)
        centroids2 = kmeans2.cluster_centers_
        colors2 = list(map(lambda x: colmap[x+1], labels2))

    # Sets the lat and long coordinates we're going to be looking at.
    plt.ylim([-100.6, -100.1])
    plt.xlim([25.5, 25.9])
    basemap = basemap_plotter()

    # Marks the centroid's latitudes and longitudes
    for i in centroids:
        centroid_lons.append(i[0])
        centroid_lats.append(i[1])

    # Same, but for the smaller centroids.
    if len(big_node_lons) > 2:
        centroid2_lons = []
        centroid2_lats = []
        for i in centroids2:
            centroid2_lons.append(float(i[0].item()))
            centroid2_lats.append(float(i[1].item()))

    # Plots the regular coordinates
    x, y = basemap(lons, lats)
    # Colors them depending on what cluster they're in
    plt.scatter(x, y, color=colors, alpha=0.5, edgecolor='k')

    # Plots the big node coordinates
    if len(big_node_lons) > 2:
        x, y = basemap(big_node_lons, big_node_lats)
        # Colors em!
        plt.scatter(x, y, color=colors2, alpha=0.5, edgecolor='k')

    #print(cluster_dict)
    #{0: 12, 1: 14, 2: 35, 3: 11, 4: 9, 5: 11, 6: 17, 7: 35, 8: 26, 9: 13, 10: 47, 11: 3, 12: 10, 13: 18, 14: 5, 15: 20, 16: 25, 17: 34}
    #[2, 7, 10, 11, 17]
    #print(global_list)

    # Plots the nodes
    x, y = basemap(centroid_lats, centroid_lons)
    i = 0
    w = 0
    while i < len(centroid_lats):
        for z in global_list:
            if z == w:
                w = w + 1
        plt.scatter(x[i], y[i], s=100, color=colmap[w+1], marker="v")
        i = i + 1
        w = w + 1

    # Plots the big nodes
    if len(big_node_lons) > 2:

        x, y = basemap(centroid2_lats, centroid2_lons)
        i = 0
        while i < len(centroid2_lats):
            plt.scatter(x[i], y[i], s=90, color=colmap[i+1], marker="v")
            i = i + 1

    # The coord dictionary will help us know which nodes have which coordinates.
        labels2 = labels2.tolist()
        labels2 = list(map(lambda x: x+num_clusters, labels2))
        labels = labels + labels2
        lats = lats + big_node_lats
        lons = lons + big_node_lons
    coord_dict = {}
    for i in labels:
        coord_dict.update({i: [[25.680723,-100.365837]]})
    for i in range(0, len(lats)):
        coord_dict[labels[i]].append([lats[i], lons[i]])
    # Adds a fancy map background :0
    basemap.arcgisimage(service='World_Street_Map', xpixels=2500, verbose=False)
    # TODO: This is a really neat way to draw lines. Might be useful very soon. basemap.plot(x, y)
    # TODO: Ask how aggressive we want to be in dropping the points that are very far away.
    # TODO: Repeating the clustering 10x and dropping each time would work.
    plt.show()
    print(coord_dict)
    return coord_dict

# TODO: If time, we need to split the city into geographic centers.
# TODO: More useful, try to split the big clusters using iterations

