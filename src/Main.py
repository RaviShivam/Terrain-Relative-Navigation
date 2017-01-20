from PIL import Image

import shownp as viewer
import Preprocessor as preprocessor
from TerrainNavigator import Navigator
import CraterDetector as craterdetector

referenceAltitude = 2000
referenceMap = "ReferenceMap.ppm"
referenceCatalogue = "finalReferenceCatalogue"

# centers = craterdetector.retrieveCraterCenterpointsAndDiameters(Image.open("../TRN/ReferenceMap.ppm"))
# add = {}
# map(lambda (k, crater): add.update({k: crater + random.gauss(0, 4)}), centers.items())
# viewer.saveData(add, "finalReferenceCatalogue")
#
# preprocessor.preprocessReferenceImage("finalReferenceCatalogue", referenceCombinations)

navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue)
navigator.locateDescentImageInReferenceImage("../data/TRN/Scene2.ppm")

