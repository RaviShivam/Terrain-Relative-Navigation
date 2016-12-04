import numpy as np
import scipy.cluster.hierarchy as hcluster
from PIL import Image
import matplotlib.pyplot as plt

import shownp as viewer

im = Image.open("training/crop3.ppm")
imagematrix = viewer.RGBToGray(np.asarray(im))
viewer.showGray(imagematrix)
threshold = 120
array = []
for i in range(0, imagematrix.shape[0]-1):
    for j in range(0, imagematrix.shape[1]-1):
        if  imagematrix[i, j] < threshold:
            imagematrix[i, j] = 0
            array.append([i, j])
        else:
            imagematrix[i, j] = 255

mat = np.array(array)
thresh = 5.5
clusters = hcluster.fclusterdata(mat, thresh, criterion="distance")
sortedclusters = {}
for i in range(0, len(clusters)-1):
    if  clusters[i] in sortedclusters.keys():
        sortedclusters[clusters[i]].append(mat[i])
    else:
        sortedclusters[clusters[i]] = [mat[i]]

print  len(sortedclusters[1])
print "centroid is x={}, y={}".format(sum(map(lambda x: x[0],sortedclusters[1]))/len(sortedclusters[1]),
                                      sum(map(lambda x: x[1],sortedclusters[1]))/len(sortedclusters[1]))



sortedclusters = {k: v for k,v in sortedclusters.iteritems() if len(v) > 4}
for (k, v) in sortedclusters.items():
    print "k={} v={}".format(k ,v)
mat = []
map(lambda (k, v): map(lambda l: mat.append([l[0], l[1]]), v), sortedclusters.items())
mat = np.array(mat)
plt.scatter(mat[:, 0], mat[:, 1])
plt.axis("equal")
plt.show()
viewer.showGray(imagematrix)







# network = Network([3,4,4,1],  alpha=0.15, beta=0.1, Lambda=0.9)
# trainingdata = [1,2,3]
# network.train(trainingdata,1)
# network.save_network(dir="network_configuration")

# def dataarray(matrix):
#     array = []
#     for i in range(512):
#         for j in range(512):
#             array.append([i, j, matrix[i][j]])
#     return array
# med = ndimage.median_filter(imagematrix, 16)
# medianfilteredimage = imagematrix - med
# viewer.showGray(medianfilteredimage)
# print imagematrix[-1,0]
#
# def getNeighbours(matrix, i, j):
#     if i==0 & j==0:
#         return np.array([matrix[1,0], matrix[0,1]])
#
#     elif i==0 & j==0:
#         return np.array([matrix[1,0], matrix[0,1]])





