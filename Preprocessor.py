import numpy as np

import math
import scipy.cluster.hierarchy as hcluster
from PIL import Image
from PIL import ImageDraw
import matplotlib.pyplot as plt

import shownp as viewer

referenceAltitude = 20000
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
    mat = []
    map(lambda (k, v): map(lambda l: mat.append([l[0], l[1]]), v), sortedclusters.items())
    # viewer.plotClusters(mat)
    return sortedclusters


def rotatePointAround(rightpoint, middlepoint):
    print "rightpoint= {}, middlepoint= {}".format(rightpoint, middlepoint)
    rotationpoint = np.array([rightpoint[0] - middlepoint[0], rightpoint[1]-middlepoint[1]])
    theta = math.radians(90)
    c, s = np.cos(theta), np.sin(theta)
    rotationMatrix = np.matrix('{} {}; {} {}'.format(c, -s, s, c))
    rotationpoint = np.dot(rotationMatrix, rotationpoint)
    rotationpoint = rotationpoint.tolist()[0]
    rotationpoint = [rotationpoint[0]+middlepoint[0], rotationpoint[1]+middlepoint[1]]
    return rotationpoint




def retrieveSemiMinorAxis(fartestpoints, middlepoint, draw):
    rightpoint =[]
    if (fartestpoints[0][0] > fartestpoints[1][0]):
        rightpoint = fartestpoints[0]
    else:
        rightpoint = fartestpoints[1]
    rotatedpoint = rotatePointAround(rightpoint, middlepoint)
    viewer.drawpoint(draw, middlepoint, 6)
    # viewer.drawpoint(draw, (rotatedpoint[1], rotatedpoint[0]), 6)



def drawFoundCraters(sortedclusters, imagematrix, im):
    draw = ImageDraw.Draw(im)
    # edges = []
    for (k, v) in sortedclusters.items():
        edgecluster = viewer.findEdges(v, imagematrix) #Retrieves map of edgepoints in each cluster.
        # map(lambda x: edges.append((x[0],x[1])),edgecluster)
        # map(lambda x: viewer.drawpoint(draw, (x[1], x[0]), 6), edgecluster)
        distance, fartestpoints = viewer.searchForFartestPoint(edgecluster) #Search for fartestpoint in cluster for diameter determination.
        viewer.drawpoint(draw, (fartestpoints[0][1],fartestpoints[0][0]), 6)
        # viewer.drawpoint(draw, fartestpoints[0], 6)
        diameter = 1.35 * distance
        a = diameter / 2
        x, y = calculateMiddlePoint(diameter, fartestpoints)
        b = retrieveSemiMinorAxis(fartestpoints, (x,y), draw)
        bbox = (x - a, y - a, x + a, y + a)
        # im = viewer.draw_ellipse(im, bbox, width=4) #Thick bounds
        draw.ellipse(bbox, fill=None, outline=400) #less thick bounds

    # viewer.plotClusters(edges)
    # del draw
    im.save("output.png")
    im.show()


def calculateMiddlePoint(diameter, fartestpoints):
    y = ((fartestpoints[0][0] + fartestpoints[1][0]) / 2) - diameter / 8
    x = ((fartestpoints[0][1] + fartestpoints[1][1]) / 2) + diameter / 4
    return x, y


def reIndexCenterPoints(centerpoints):
    counter = 1
    sortedcenterpoints = {}
    for (k,v) in centerpoints.items():
        sortedcenterpoints[counter] = v
        counter += 1
    return sortedcenterpoints

def retrieveAllClusterCenterPoints(sortedclusters, imagematrix):
    centerpoints = {}
    diameters = {}
    for (k, v) in sortedclusters.items():
        edgecluster = viewer.findEdges(v, imagematrix)
        val = viewer.searchForFartestPoint(edgecluster)
        middlepoints = val[1]
        diameter = 1.35 * val[0]
        y = ((middlepoints[0][0] + middlepoints[1][0]) / 2) - diameter / 8
        x = ((middlepoints[0][1] + middlepoints[1][1]) / 2) + diameter / 4
        centerpoints[k] = np.array([x, y])
        diameters[k] = diameter
    return reIndexCenterPoints(centerpoints), diameters

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
        allcombinationnormvectors[k] = []
        for (k2, point2) in centerpoints.items():
            if (point[0] == point2[0] and point[1] == point2[1]):
                continue
            else:
                vect = (point2 - point) / np.linalg.norm(point2 - point)
                allcombinationnormvectors[k].append(vect)
    return allcombinationnormvectors


def retrievAllNormVectorsFromReference():
    im = Image.open("TRN/ReferenceMap.ppm")
    array, imagematrix = applyPrimaryIlluminationFilter(im)
    sortedclusters = retrieveCraterClusters(array)
    # centerpoints = drawFoundCraters(sortedclusters,imagematrix, im)
    centerpoints, diameters = retrieveAllClusterCenterPoints(sortedclusters, imagematrix)
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


def drawDescentImage(upperleftpoint, upperrightpoint, lowerleftpoint, lowerrightpoint, middlepoint):
    refimage = Image.open("TRN/ReferenceMap.ppm")
    draw = ImageDraw.Draw(refimage)
    draw.line((upperleftpoint[0],upperleftpoint[1], upperrightpoint[0], upperrightpoint[1]), fill = 128, width=5)
    draw.line((upperleftpoint[0],upperleftpoint[1], lowerleftpoint[0], lowerleftpoint[1]), fill = 128, width=5)
    draw.line((lowerleftpoint[0],lowerleftpoint[1], lowerrightpoint[0], lowerrightpoint[1]), fill = 128, width=5)
    draw.line((lowerrightpoint[0],lowerrightpoint[1], upperrightpoint[0], upperrightpoint[1]), fill = 128, width=5)
    draw.line((middlepoint[0],middlepoint[1]-1, middlepoint[0], middlepoint[1]+1), fill = 128, width= 12)
    draw.line((middlepoint[0]-1,middlepoint[1], middlepoint[0]+1, middlepoint[1]), fill = 128, width= 12)
    # refimage.show()


def locateDescentImageInReferenceImage(imagename):
    # allPossibleCombinations = retrievAllNormVectorsFromReference()
    # viewer.saveCombinations(allPossibleCombinations, "combinations")

    allPossibleCombinations = viewer.readCombinations("combinations")
    referenceCenterpoints = viewer.readCombinations("centerpoints")
    im = Image.open(imagename)
    centerpoints = retrieveCraterCenterpointsAndDiameters(im)
    verificationcrater = centerpoints[3]
    smallSet = oneCombinationNormVector(verificationcrater, centerpoints)
    referencecrater = 0
    for (k,values) in allPossibleCombinations.items():
        if (isSubsetOf(smallSet, values, 0.1)):
            referencecrater = referenceCenterpoints[k]
            break
    # s = verificationcrater[2]/referencecrater[2]
    s = 2
    r = np.array([referencecrater[0],referencecrater[1]])
    v = np.array([verificationcrater[0], verificationcrater[1]])
    upperleftpoint = r - (v/s)
    lowerrightpoint = [r[0] + (512 - v[0])/s, r[1] + (512 - v[1])/s]
    upperrightpoint = [r[0] + (512 - v[0])/s, r[1] - v[1]/s]
    lowerleftpoint = [r[0] - v[0]/s, r[1] + (512 - v[1])/s]
    middlepoint = (upperleftpoint+lowerleftpoint+upperrightpoint+lowerrightpoint)/4

    drawDescentImage(upperleftpoint, upperrightpoint, lowerleftpoint, lowerrightpoint, middlepoint)


def retrieveCraterCenterpointsAndDiameters(im):
    array, imagematrix = applyPrimaryIlluminationFilter(im)
    sortedclusters = retrieveCraterClusters(array)
    drawFoundCraters(sortedclusters,imagematrix, im)
    centerpoints, diameters = retrieveAllClusterCenterPoints(sortedclusters, imagematrix)
    return centerpoints


#



# retrievAllNormVectorsFromReference()
locateDescentImageInReferenceImage("TRN/Scene1.ppm")
# locateDescentImageInReferenceImage("TRN/Scene2.ppm")
# locateDescentImageInReferenceImage("TRN/Scene3.ppm")
# locateDescentImageInReferenceImage("TRN/Scene4.ppm")



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
