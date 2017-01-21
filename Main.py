import sys

from src.TerrainNavigator import Navigator

referenceAltitude = 2000

referenceMap = "ReferenceMap.ppm"
referenceCatalogue = "finalReferenceCatalogue"
defaultDescentImages = ["Scene1.ppm", "Scene2.ppm", "Scene3.ppm", "Scene4.ppm"]
defaultDataPath = "../data/TRN/"

args = len(sys.argv)
arguments = str(sys.argv)

if (args is 1 or args is 0):
    navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue)
    for descentimage in defaultDescentImages:
        navigator.locateDescentImageInReferenceImage(defaultDataPath + descentimage)


# centers = craterdetector.retrieveCraterCenterpointsAndDiameters(Image.open("../TRN/ReferenceMap.ppm"))
# add = {}
# map(lambda (k, crater): add.update({k: crater + random.gauss(0, 4)}), centers.items())
# viewer.saveData(add, "finalReferenceCatalogue")
#
# preprocessor.preprocessReferenceImage("finalReferenceCatalogue", referenceCombinations)


