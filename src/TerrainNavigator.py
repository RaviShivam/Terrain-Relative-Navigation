from PIL import Image

import numpy as np
from PIL import ImageDraw

import Preprocessor as preprocessor
import shownp as viewer
import CraterDetector as craterDetector

referenceAltitude = 20000

def oneCombinationNormVector(point, centerpoints):
    normvectors = []
    for (k2, point2) in centerpoints.items():
        if (point[0] == point2[0] and point[1] == point2[1]):
            continue
        else:
            vect = (point2 - point) / np.linalg.norm(point2 - point)
            normvectors.append(vect)
    return normvectors

def drawDescentImageOnReferenceImage(upperleftpoint, upperrightpoint, lowerleftpoint, lowerrightpoint, middlepoint):
    """

    :param upperleftpoint:
    :param upperrightpoint:
    :param lowerleftpoint:
    :param lowerrightpoint:
    :param middlepoint:
    :return:
    """
    refimage = Image.open("../TRN/ReferenceMap.ppm")
    draw = ImageDraw.Draw(refimage)
    draw.line((upperleftpoint[0], upperleftpoint[1], upperrightpoint[0], upperrightpoint[1]), fill = 128, width=5)
    draw.line((upperleftpoint[0], upperleftpoint[1], lowerleftpoint[0], lowerleftpoint[1]), fill = 128, width=5)
    draw.line((lowerleftpoint[0], lowerleftpoint[1], lowerrightpoint[0], lowerrightpoint[1]), fill = 128, width=5)
    draw.line((lowerrightpoint[0], lowerrightpoint[1], upperrightpoint[0], upperrightpoint[1]), fill = 128, width=5)
    draw.line((middlepoint[0], middlepoint[1]-1, middlepoint[0], middlepoint[1]+1), fill = 128, width= 12)
    draw.line((middlepoint[0]-1, middlepoint[1], middlepoint[0]+1, middlepoint[1]), fill = 128, width= 12)
    refimage.show()

def locateDescentImageInReferenceImage(imagename):
    allPossibleCombinations = viewer.loadData("combinations")
    # reference_catalogue = viewer.loadData("referenceCatalogue")
    centerpoints = viewer.loadData("addfile")
    # centerpoints = preprocessor.extractCenterpoints(reference_catalogue)
    im = Image.open(imagename)
    descentImageCatalogue = craterDetector.retrieveCraterCenterpointsAndDiameters(im)
    verificationcrater = descentImageCatalogue[3]
    smallSet = oneCombinationNormVector(verificationcrater, descentImageCatalogue)
    referencecrater = 0
    for (k,values) in allPossibleCombinations.items():
        if (isSubsetOf(smallSet, values, 0.1)):
            referencecrater = centerpoints[k]
            break
    # s = verificationcrater[2]/referencecrater[2]
    s = 2
    r = np.array([referencecrater[0], referencecrater[1]])
    v = np.array([verificationcrater[0], verificationcrater[1]])
    upperleftpoint = r - (v/s)
    lowerrightpoint = [r[0] + (512 - v[0])/s, r[1] + (512 - v[1])/s]
    upperrightpoint = [r[0] + (512 - v[0])/s, r[1] - v[1]/s]
    lowerleftpoint = [r[0] - v[0]/s, r[1] + (512 - v[1])/s]
    middlepoint = (upperleftpoint+lowerleftpoint+upperrightpoint+lowerrightpoint)/4

    drawDescentImageOnReferenceImage(upperleftpoint, upperrightpoint, lowerleftpoint, lowerrightpoint, middlepoint)

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
    print matchesfound
    if (matchesfound == len(smallSet)):
        return True
    else:
        return False

def isAlmostEquals(vector, refvector, threshold):
    if (((vector[0] - threshold < refvector[0]) and (vector[0] + threshold > refvector[0])) and
            ((vector[1] - threshold < refvector[1]) and (vector[1] + threshold > refvector[1]))
        ): return True
    else: return False

