import numpy as np
import scipy.cluster.hierarchy as hcluster
from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
from scipy import ndimage, random

import shownp as viewer
import EllipseFitter as ellipsefitter
from Crater import ClusterCrater
from Crater import Crater

primaryFilterTreshold = 120
secondaryFilterThreshold = 240


def applyPrimaryIlluminationFilter(im):
    """
    Uses predefined threshold to filter out pixels with lower gray-scale value

    [1] All gray-scale values lower than a threshold are set to 0
    [2] All gray-scale values higher than a threshold are set to 255 (max)

    :param im: The image file that needs to be filtered.
    :return: array (list) = list of all the pixels set to 0. imagematrix (ndarray) = matrix of the image with values either 0 of 255.
    """
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
    # Uncomment this next line of code to view the intermediate result of the filter.
    # viewer.showGray(imagematrix)
    return array, imagematrix


def retrieveCraterClusters(array):
    """
    Uses hierarchical clustering to cluster pixels on an image that have values 0
    assigned to them.
    :param array: list of all the points that have value 0 assigned to them.
    :return: hashmap of all the clusters sorted by index.
    """
    mat = np.array(array)
    thresh = 5.5
    clusters = hcluster.fclusterdata(mat, thresh, criterion="distance")
    sortedclusters = {}
    for i in range(0, len(clusters) - 1):
        if clusters[i] in sortedclusters.keys():
            sortedclusters[clusters[i]].append(mat[i])
        else:
            sortedclusters[clusters[i]] = [mat[i]]
    sortedclusters = {k: v for k, v in sortedclusters.iteritems() if len(v) > 12}
    ### Uncomment this section to plot the clusters.
    # mat = []
    # map(lambda (k, v): map(lambda l: mat.append([l[0], l[1]]), v), sortedclusters.items())
    # viewer.plotClusters(mat)
    ###
    return reIndexCenterPoints(sortedclusters)

def reIndexCenterPoints(centerpoints):
    """
    Helper method to rearrange missing cluster points in the given hashmap.
    This method is only to be accessed by methods in this module and not intented to be accesed arbitrarily.
    :param centerpoints: All the centerpoints of the craters in an image that needs sorting.
    :return: sorted cluster points.
    """
    counter = 1
    sortedcenterpoints = {}
    for (k, v) in centerpoints.items():
        sortedcenterpoints[counter] = v
        counter += 1
    return sortedcenterpoints

def retrieveAllClusterCenterPoints(sortedclusters, imagematrix):
    """
    Processes the clusters and returns list of all the centerpoints of the craters found in an image.
    :param sortedclusters: Clusters found on a the image
    :param imagematrix: original image in matrix form
    :return: return all the centerpoints and initial diameters of the
    """
    craters = {}
    for (k, v) in sortedclusters.items():
        edgecluster = viewer.findEdges(v, imagematrix)
        distance, fartestpoints = viewer.searchForFartestPoint(edgecluster) #Search for fartestpoint in cluster for diameter determination.
        diameter = 1.35 * distance
        x, y = viewer.calculateMiddlePoint(diameter, fartestpoints)
        centerpoint = np.array([x, y])
        craters[k] = Crater(k, centerpoint, diameter)
    return craters


def extractCraters(im):
    """
    This method is only to be accessed by methods in this module and not intented to be accessed arbitrarily.
    :param im: image that needs to be processed and retrieve respective diameters.
    :return: centerpoint and the diameters of all the craters in the given image.
    """
    array, imagematrix = applyPrimaryIlluminationFilter(im)
    sortedclusters = retrieveCraterClusters(array)
    craters = retrieveAllClusterCenterPoints(sortedclusters, imagematrix)
    # ellipsefitter.drawFoundCraters(sortedclusters, imagematrix, im)
    return craters





"""
This part of the code is NOT used for the actual program. Rather, was tried to be implemented but did not succeed.
"""

def secondaryIlluminationFilter(im):
    """
    Uses predefined threshold to filter out pixels with lower gray-scale value

    [1] All gray-scale values lower than a threshold are set to 0
    [2] All gray-scale values higher than a threshold are set to 255 (max)

    :param im: The image file that needs to be filtered.
    :return: array (list) = list of all the pixels set to 0. imagematrix (ndarray) = matrix of the image with values either 0 of 255.
    """
    global secondaryFilterThreshold
    array = []
    imagematrix = viewer.RGBToGray(np.asarray(im))
    for i in range(0, imagematrix.shape[0] - 1):
        for j in range(0, imagematrix.shape[1] - 1):
            if imagematrix[i, j] > secondaryFilterThreshold:
                imagematrix[i, j] = 255
                array.append([i, j])
            else:
                imagematrix[i, j] = 0
    med = ndimage.median_filter(imagematrix, 6)
    # viewer.showGray(med)
    return array, imagematrix


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def correlateClusters(clusters1, clusters2, draw):
    clusters1 = map(lambda x: ClusterCrater(x[0], x[1]), clusters1.items())
    clusters2 = map(lambda x: ClusterCrater(x[0], x[1]), clusters2.items())
    # for cluster in clusters1:
    cluster = clusters1[4]
    for secondcluster in clusters2:
        draw.line((cluster.centerpoint[0], cluster.centerpoint[1], secondcluster.centerpoint[0], secondcluster.centerpoint[1]), fill = 128, width=1)



def tryDoubleFilter():
    im = Image.open("../data/TRN/ReferenceMap.ppm")
    # font = ImageFont.truetype("sans-serif.ttf", 14)
    im = trim(im)
    draw = ImageDraw.Draw(im)
    array1, med1 = applyPrimaryIlluminationFilter(im)
    array2, med2 = secondaryIlluminationFilter(im)
    cluster1 = retrieveCraterClusters(array1)
    cluster2 = retrieveCraterClusters(array2)
    correlateClusters(cluster1, cluster2, draw)
    im.show()


