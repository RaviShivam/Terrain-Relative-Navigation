import numpy as np

from PIL import Image

import shownp as viewer
import CraterDetector as craterDetector


def allCombinationNormVectors(centerpoints):
    allcombinationnormvectors = {}
    for (k, point) in centerpoints.items():
        allcombinationnormvectors[k] = []
        for (k2, point2) in centerpoints.items():
            if (point[0] == point2[0] and point[1] == point2[1]):
                continue
            else:
                vect = (point2 - point) / np.linalg.norm(point2 - point)
                allcombinationnormvectors[k].append(vect)
    return allcombinationnormvectors

def retrievAllNormVectorsFromReference():
    referenceCatolog = viewer.loadData("referenceCatalogue")
    centerpoints = {}
    map(lambda (k, v): centerpoints.update({k: v.centerpoint}), referenceCatolog.items())
    return allCombinationNormVectors(centerpoints)

def preprocessReferenceImage(catalogue, combinations):
    allPossibleCombinations = retrievAllNormVectorsFromReference()
    print allPossibleCombinations
    viewer.saveData(allPossibleCombinations, "combinations")

    allPossibleCombinations = viewer.loadData("combinations")
    referenceCenterpoints = viewer.loadData("centerpoints")






#### Neural Network#####
# testdat = [sum(map(lambda x: x[0],sortedclusters[1]))/len(sortedclusters[1]), sum(map(lambda x: x[1],sortedclusters[1]))/len(sortedclusters[1])]
# diameter = np.sqrt(len(sortedclusters[1])/3.14)*2
# print diameter
# print "centroidin is x={}, y={}".format(testdat[0], testdat[1])
#
# testdat.append(diameter)
# testdat.append(testdat[0]*testdat[0])
# testdat.append(testdat[1]*testdat[1])
# network = Network([5,6,4,2],  alpha=0.1, beta=0.1, Lambda=0.9)
# network.read_network(dir="centroid_configuration")
# print network.feed(testdat)*57

### Attempt for median filter#####

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
