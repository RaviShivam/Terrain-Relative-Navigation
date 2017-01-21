from PIL import Image

import numpy as np
from PIL import ImageDraw

import Preprocessor as preprocessor
import shownp as viewer
import CraterDetector as craterDetector

class Navigator:
    def __init__(self, referenceAltitude, referenceMap, referenceCatalogue):
        """
        Initializes an instance of Navigator object which preprocesses the referenceMap automatically.
        By creating a Navigator object once, it makes it possible to detect consecutive images without
        preprocessing it.
        :param referenceAltitude: The altitude at which the reference image is given
        :param referenceMap: The name of the reference map.
        :param referenceCatalogue: The catalogue of the reference image. This contains all the centerpoints of all the craters
        and their diameters.
        """
        self.referenceAltitude = referenceAltitude
        self.referenceMap = referenceMap
        self.referenceCatalogue = referenceCatalogue
        self.referenceCombinations = referenceCatalogue + "Combinations"
        preprocessor.preprocessReferenceImage(self.referenceCatalogue, self.referenceCombinations)

    def oneCombinationUnitVector(self, point, centerpoints):
        """
        Takes one point in a given list of points and calculates all the unit vectors to the other centerpoints
        in the list.
        This method is only to be accessed by methods in this module and not intented to be accesed arbitrarily.
        :param point: point from where all the other relative positions should be calculated
        :param centerpoints: list of all the centpoints that needs to be processed.
        :return: unit vectors every other centerpoint of craters in the image.
        """
        unitvectors = []
        for (k2, point2) in centerpoints.items():
            if (point[0] == point2[0] and point[1] == point2[1]):
                continue
            else:
                vect = (point2 - point) / np.linalg.norm(point2 - point)
                unitvectors.append(vect)
        return unitvectors

    def drawDescentImageOnReferenceImage(self, upperleftpoint, upperrightpoint, lowerleftpoint, lowerrightpoint, middlepoint):
        """
        Draws the specified coordinates of the landers location on to the reference map.
        This method is only to be accessed by methods in this module and not intented to be accesed arbitrarily.
        :param upperleftpoint: upperleft point in the reference image
        :param upperrightpoint: upperright point in the reference image
        :param lowerleftpoint: lowerleft point in the reference image
        :param lowerrightpoint: lower right point in reference
        :param middlepoint: Exact location of the lander on the reference image.
        :return: Null
        """
        refimage = Image.open("../data/TRN/ReferenceMap.ppm")
        # font = ImageFont.truetype("sans-serif.ttf", 14)
        draw = ImageDraw.Draw(refimage)
        draw.line((upperleftpoint[0], upperleftpoint[1], upperrightpoint[0], upperrightpoint[1]), fill = 128, width=5)
        draw.line((upperleftpoint[0], upperleftpoint[1], lowerleftpoint[0], lowerleftpoint[1]), fill = 128, width=5)
        draw.line((lowerleftpoint[0], lowerleftpoint[1], lowerrightpoint[0], lowerrightpoint[1]), fill = 128, width=5)
        draw.line((lowerrightpoint[0], lowerrightpoint[1], upperrightpoint[0], upperrightpoint[1]), fill = 128, width=5)
        draw.line((middlepoint[0], middlepoint[1]-1, middlepoint[0], middlepoint[1]+1), fill = 128, width= 12)
        draw.line((middlepoint[0]-1, middlepoint[1], middlepoint[0]+1, middlepoint[1]), fill = 128, width= 12)
        text = "Middlepoint is {} and altitude is {} km".format(middlepoint, 100)
        draw.text((0, 0), text, (20, 86, 169))
        refimage.show()


    def executePatternRecognition(self, allPossibleCombinations, centerpoints, descentImageCatalogue):
        """
        This part actually executes the pattern recognition on the reference map.
        This method is only to be accessed by methods in this module and not intented to be accesed arbitrarily.
        :param allPossibleCombinations: Dictionary of all craters containing the relative distances to every other crater on the image
        :param centerpoints: centerpoint are the catalogued centerpoints of all the craters in the reference map
        :param descentImageCatalogue: list of all the crater centerpoints and diameters in the descent image.
        :return: The approximate location of the lander on top of the referenceMap.
        """
        verificationcrater = descentImageCatalogue[3]
        smallSet = self.oneCombinationUnitVector(verificationcrater, descentImageCatalogue)
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
        """
        Evaluates whether a smaller set of unit vectors is a subset of a larger set. It does this by allowing a certain error,
        as the unit vectors in a reference image may not be exactly the same as in the detected image.
        This method is only to be accessed by methods in this module and not intented to be accesed arbitrarily.
        :param smallSet: Set containing unit vectors of a certain crater in the descent image.
        :param values: Set containing unit vectors of a certain crater in the reference image.
        :param threshold: Error factor that can be tolerated. If the error is higher than this, the vectors are not the same.
        :return: If the smaller set is identified to be a subset of the larger set, it returs true, else it returns false.
        """
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
        if (matchesfound == len(smallSet)):
            return True
        else:
            return False

    def isAlmostEquals(self, vector, refvector, threshold):
        """
        Compares 2 different unit vector to verify whether they have almost the same direction. This is done by including
        a small error factor which allows for flexibility.
        This method is only to be accessed by methods in this module and not intented to be accesed arbitrarily.
        :param vector: First vector to be compared.
        :param refvector: Second vector with which the first vector is compared to check for equality.
        :param threshold: Error factor that can be tolerated. If the error is higher than this, the vectors are not the same.
        :return: If the smaller set is identified to be a subset of the larger set, it returs true, else it returns false.
        """
        if (((vector[0] - threshold < refvector[0]) and (vector[0] + threshold > refvector[0])) and
                ((vector[1] - threshold < refvector[1]) and (vector[1] + threshold > refvector[1]))
            ): return True
        else: return False

    def locateDescentImageInReferenceImage(self, imagename):
        """
        This method uses the preprocessed referencemap to locate the descent image. It provides the coordinates
        and altitude on the image produced.
        :param imagename: the descent image which needs to be located in the reference map.
        :return: None
        """
        centerpoints = viewer.loadData(self.referenceCatalogue)
        allPossibleCombinations = viewer.loadData(self.referenceCombinations)
        # reference_catalogue = viewer.loadData("referenceCatalogue")
        # centerpoints = preprocessor.extractCenterpoints(reference_catalogue)
        im = Image.open(imagename)
        descentImageCatalogue = craterDetector.retrieveCraterCenterpointsAndDiameters(im)
        self.executePatternRecognition(allPossibleCombinations, centerpoints, descentImageCatalogue)

