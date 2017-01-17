from PIL import Image

import numpy as np
from PIL import ImageDraw

import Preprocessor as preprocessor
import shownp as viewer
import CraterDetector as craterDetector

class Navigator:
    def __init__(self, referenceAltitude, referenceMap, referenceCatalogue):
        self.referenceAltitude = referenceAltitude
        self.referenceMap = referenceMap
        self.referenceCatalogue = referenceCatalogue
        self.referenceCombinations = referenceCatalogue + "Combinations"
        preprocessor.preprocessReferenceImage(referenceCatalogue, self.referenceCombinations)

    def oneCombinationNormVector(self, point, centerpoints):
        normvectors = []
        for (k2, point2) in centerpoints.items():
            if (point[0] == point2[0] and point[1] == point2[1]):
                continue
            else:
                vect = (point2 - point) / np.linalg.norm(point2 - point)
                normvectors.append(vect)
        return normvectors

    def drawDescentImageOnReferenceImage(self, upperleftpoint, upperrightpoint, lowerleftpoint, lowerrightpoint, middlepoint):
        """
        Draws the specified coordinates of the landers location on to the reference map.
        :param upperleftpoint: upperleft point in the reference image
        :param upperrightpoint: upperright point in the reference image
        :param lowerleftpoint: lowerleft point in the reference image
        :param lowerrightpoint: lower right point in reference
        :param middlepoint: Exact location of the lander on the reference image.
        :return: Null
        """
        refimage = Image.open("../data/TRN/ReferenceMap.ppm")
        draw = ImageDraw.Draw(refimage)
        draw.line((upperleftpoint[0], upperleftpoint[1], upperrightpoint[0], upperrightpoint[1]), fill = 128, width=5)
        draw.line((upperleftpoint[0], upperleftpoint[1], lowerleftpoint[0], lowerleftpoint[1]), fill = 128, width=5)
        draw.line((lowerleftpoint[0], lowerleftpoint[1], lowerrightpoint[0], lowerrightpoint[1]), fill = 128, width=5)
        draw.line((lowerrightpoint[0], lowerrightpoint[1], upperrightpoint[0], upperrightpoint[1]), fill = 128, width=5)
        draw.line((middlepoint[0], middlepoint[1]-1, middlepoint[0], middlepoint[1]+1), fill = 128, width= 12)
        draw.line((middlepoint[0]-1, middlepoint[1], middlepoint[0]+1, middlepoint[1]), fill = 128, width= 12)
        refimage.show()

    def locateDescentImageInReferenceImage(self, imagename):
        """
        Locates a given
        :param imagename:
        :param catalogue:
        :return:
        """
        centerpoints = viewer.loadData(self.referenceCatalogue)
        allPossibleCombinations = viewer.loadData(self.referenceCombinations)
        # reference_catalogue = viewer.loadData("referenceCatalogue")
        # centerpoints = preprocessor.extractCenterpoints(reference_catalogue)
        im = Image.open(imagename)
        descentImageCatalogue = craterDetector.retrieveCraterCenterpointsAndDiameters(im)
        self.executePatternRecognition(allPossibleCombinations, centerpoints, descentImageCatalogue)

    def executePatternRecognition(self, allPossibleCombinations, centerpoints, descentImageCatalogue):
        """
        This part actually executes the pattern recognition on the reference map. This method is only to be used by methods in this
        class and not intented to be accesed arbitrarily.
        :param allPossibleCombinations: Dictionary of all craters containing the relative distances to every other crater on the image
        :param centerpoints: centerpoint are the catalogued centerpoints of all the craters in the reference map
        :param descentImageCatalogue: list of all the crater centerpoints and diameters in the descent image.
        :return: The approximate location of the lander on top of the referenceMap.
        """
        verificationcrater = descentImageCatalogue[3]
        smallSet = self.oneCombinationNormVector(verificationcrater, descentImageCatalogue)
        referencecrater = 0
        for (k, values) in allPossibleCombinations.items():
            if (self.isSubsetOf(smallSet, values, 0.1)):
                referencecrater = centerpoints[k]
                break
        s = 2
        r = np.array([referencecrater[0], referencecrater[1]])
        v = np.array([verificationcrater[0], verificationcrater[1]])
        upperleftpoint = r - (v / s)
        lowerrightpoint = [r[0] + (512 - v[0]) / s, r[1] + (512 - v[1]) / s]
        upperrightpoint = [r[0] + (512 - v[0]) / s, r[1] - v[1] / s]
        lowerleftpoint = [r[0] - v[0] / s, r[1] + (512 - v[1]) / s]
        middlepoint = (upperleftpoint + lowerleftpoint + upperrightpoint + lowerrightpoint) / 4
        self.drawDescentImageOnReferenceImage(upperleftpoint, upperrightpoint, lowerleftpoint, lowerrightpoint,
                                              middlepoint)
        return middlepoint

    def isSubsetOf(self, smallSet, values, threshold):
        matchesfound = 0
        for vector in smallSet:
            vectorequal = False
            for refvector in values:
                if (self.isAlmostEquals(vector, refvector, threshold)):
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

    def isAlmostEquals(self, vector, refvector, threshold):
        if (((vector[0] - threshold < refvector[0]) and (vector[0] + threshold > refvector[0])) and
                ((vector[1] - threshold < refvector[1]) and (vector[1] + threshold > refvector[1]))
            ): return True
        else: return False

