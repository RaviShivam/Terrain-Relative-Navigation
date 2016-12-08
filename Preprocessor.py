import numpy as np

import scipy.cluster.hierarchy as hcluster
from PIL import Image
from PIL import ImageDraw

import shownp as viewer

primaryFilterTreshold = 120


def applyPrimaryIlluminationFilter(im):
    global primaryFilterTreshold
    array = []
    imagematrix = viewer.RGBToGray(np.asarray(im))
    for i in range(0, imagematrix.shape[0] - 1):
        for j in range(0, imagematrix.shape[1] - 1):
            if imagematrix[i, j] < primaryFilterTreshold:
                imagematrix[i, j] = 0
                array.append([i, j])
            else:
                imagematrix[i, j] = 255
    # viewer.showGray(imagematrix)
    return array, imagematrix


def retrieveCraterClusters(array):
    mat = np.array(array)
    thresh = 5.5
    clusters = hcluster.fclusterdata(mat, thresh, criterion="distance")
    sortedclusters = {}
    for i in range(0, len(clusters) - 1):
        if clusters[i] in sortedclusters.keys():
            sortedclusters[clusters[i]].append(mat[i])
        else:
            sortedclusters[clusters[i]] = [mat[i]]
    sortedclusters = {k: v for k, v in sortedclusters.iteritems() if len(v) > 8}
    return sortedclusters


def drawFoundCraters(sortedclusters, imagematrix, im):
    centerpoints = {}
    draw = ImageDraw.Draw(im)
    for (k, v) in sortedclusters.items():
        edgecluster = viewer.findEdges(v, imagematrix)
        val = viewer.searchForFartestPoint(edgecluster)
        middlepoints = val[1]
        diameter = 1.35 * val[0]
        # diameter = (4*np.sqrt(len(v)/3.14) + 1.4*val[0])/2
        # diameter = (4*np.sqrt(len(v)/3.14) + 1.4*val[0])/2
        r = diameter / 2
        y = ((middlepoints[0][0] + middlepoints[1][0]) / 2) - diameter / 8
        x = ((middlepoints[0][1] + middlepoints[1][1]) / 2) + diameter / 4
        centerpoints[k] = np.array([x, y])
        bbox = (x - r, y - r, x + r, y + r)
        draw.ellipse(bbox, fill=None, outline=400)

    # Draw circels around craters
    del draw
    im.save("output.png")
    im.show()
    return centerpoints

def reIndexCenterPoints(centerpoints):
    counter = 1
    sortedcenterpoints = {}
    for (k,v) in centerpoints.items():
        sortedcenterpoints[counter] = v
        counter += 1
    return sortedcenterpoints

def retrieveAllClusterCenterPoints(sortedclusters, imagematrix):
    centerpoints = {}
    for (k, v) in sortedclusters.items():
        edgecluster = viewer.findEdges(v, imagematrix)
        val = viewer.searchForFartestPoint(edgecluster)
        middlepoints = val[1]
        diameter = 1.35 * val[0]
        y = ((middlepoints[0][0] + middlepoints[1][0]) / 2) - diameter / 8
        x = ((middlepoints[0][1] + middlepoints[1][1]) / 2) + diameter / 4
        centerpoints[k] = np.array([x, y, diameter])
    return reIndexCenterPoints(centerpoints)

def oneCombinationNormVector(point, centerpoints):
    normvectors = []
    for (k2, point2) in centerpoints.items():
        if (point[0] == point2[0] and point[1] == point2[1]):
            continue
        else:
            vect = (point2 - point) / np.linalg.norm(point2 - point)
            normvectors.append(vect)
    return normvectors

def allCombinationNormVectors(centerpoints):
    allcombinationnormvectors = {}
    for (k, point) in centerpoints.items():
        allcombinationnormvectors[(point.tolist()[0], point.tolist()[1])] = []
        for (k2, point2) in centerpoints.items():
            if (point[0] == point2[0] and point[1] == point2[1]):
                continue
            else:
                vect = (point2 - point) / np.linalg.norm(point2 - point)
                allcombinationnormvectors[point.tolist()[0], point.tolist()[1]].append(vect)
    return allcombinationnormvectors


def retrievAllNormVectorsFromReference():
    im = Image.open("TRN/ReferenceMap.ppm")
    array, imagematrix = applyPrimaryIlluminationFilter(im)
    sortedclusters = retrieveCraterClusters(array)
    # centerpoints = drawFoundCraters(sortedclusters,imagematrix, im)
    centerpoints = retrieveAllClusterCenterPoints(sortedclusters, imagematrix)
    viewer.saveCombinations(centerpoints, "centerpoints")
    return allCombinationNormVectors(centerpoints)


def isAlmostEquals(vector, refvector, threshold):
    if (((vector[0] - threshold < refvector[0]) and (vector[0] + threshold > refvector[0])) and
        ((vector[1] - threshold < refvector[1]) and (vector[1] + threshold > refvector[1]))
        ): return True
    else: return False


def isSubsetOf(smallSet, values, threshold):
    matchesfound = 0
    for vector in smallSet:
        vectorequal = False
        for refvector in values:
            if (isAlmostEquals(vector, refvector, threshold)):
                vectorequal = True
                matchesfound += 1
                break;
        if not(vectorequal):
            break;
    if (matchesfound == len(smallSet)):
        return True
    else:
        return False


def locateDescentImageInReferenceImage(imagename):
    # allPossibleCombinations = retrievAllNormVectorsFromReference()
    # viewer.saveCombinations(allPossibleCombinations, "combinations")

    allPossibleCombinations = viewer.readCombinations()

    im = Image.open(imagename)
    array,imagematrix = applyPrimaryIlluminationFilter(im)
    # viewer.showGray(imagematrix)
    sortedclusters = retrieveCraterClusters(array)
    # drawFoundCraters(sortedclusters,imagematrix, im)
    centerpoints = retrieveAllClusterCenterPoints(sortedclusters, imagematrix)
    verificationpoint = centerpoints[len(centerpoints)]
    smallSet = oneCombinationNormVector(verificationpoint, centerpoints)
    for (k,values) in allPossibleCombinations.items():
        if (isSubsetOf(smallSet, values, 0.1)):
            print k
            print verificationpoint
#



# retrievAllNormVectorsFromReference()
locateDescentImageInReferenceImage("TRN/Scene1.ppm")



# for (k, v) in edgecluster.items():
#     print "k={} v={}".format(k ,v)
# mat = []
# map(lambda (k, v): map(lambda l: mat.append([l[0], l[1]]), v), edgecluster.items())
# mat = np.array(mat)
# plt.scatter(mat[:, 0], mat[:, 1])
# plt.axis("equal")
# plt.show()

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
