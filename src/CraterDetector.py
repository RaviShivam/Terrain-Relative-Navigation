import numpy as np
import scipy.cluster.hierarchy as hcluster
import shownp as viewer

import Preprocessor as preprocessor

primaryFilterTreshold = 120

def applyPrimaryIlluminationFilter(im):
    """
    Uses predefined threshold to filter out pixels with lower gray-scale value

    [1] All gray-scale values lower than a threshold are set to 0
    [2] All gray-scale values higher than a threshold are set to 255 (max)

    Parameters
    ----------
    im (Image) = The image file that needs to be filtered.

    Return
    ------
    array (list) = list of all the pixels set to 0.
    imagematrix (ndarray) = matrix of the image with values either 0 of 255.

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
    # viewer.showGray(imagematrix)
    return array, imagematrix

def retrieveCraterClusters(array):
    """
    Uses hierarchical clustering to cluster pixels on an image that have values 0
    assigned to them.

    Parameter
    ---------
    array (list) = list of all the points that have value 0 assigned to them

    Return
    ------
    sortedcluster = hashmap of all the clusters sorted by index.

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
    sortedclusters = {k: v for k, v in sortedclusters.iteritems() if len(v) > 8}
    # ### Uncomment this section to plot the clusters.
    # mat = []
    # map(lambda (k, v): map(lambda l: mat.append([l[0], l[1]]), v), sortedclusters.items())
    # viewer.plotClusters(mat)
    # ###
    return sortedclusters

def reIndexCenterPoints(centerpoints):
    counter = 1
    sortedcenterpoints = {}
    for (k, v) in centerpoints.items():
        sortedcenterpoints[counter] = v
        counter += 1
    return sortedcenterpoints


def retrieveAllClusterCenterPoints(sortedclusters, imagematrix):
    centerpoints = {}
    diameters = {}
    for (k, v) in sortedclusters.items():
        edgecluster = viewer.findEdges(v, imagematrix)
        distance, fartestpoints = viewer.searchForFartestPoint(edgecluster) #Search for fartestpoint in cluster for diameter determination.
        diameter = 1.35 * distance
        x, y = viewer.calculateMiddlePoint(diameter, fartestpoints)
        centerpoints[k] = np.array([x, y])
        diameters[k] = diameter
    return reIndexCenterPoints(centerpoints), diameters

def retrieveCraterCenterpointsAndDiameters(im):
    array, imagematrix = preprocessor.applyPrimaryIlluminationFilter(im)
    sortedclusters = preprocessor.retrieveCraterClusters(array)
    centerpoints, diameters = retrieveAllClusterCenterPoints(sortedclusters, imagematrix)
    return centerpoints
