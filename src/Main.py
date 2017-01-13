from PIL import Image

import shownp as viewer
import Preprocessor as preprocessor
import TerrainNavigator as navigator
import CraterDetector as craterdetector

referenceCatalogue = "finalReferenceCatalogue"
referenceCombinations = "combinations"

# centers = craterdetector.retrieveCraterCenterpointsAndDiameters(Image.open("../TRN/ReferenceMap.ppm"))
# add = {}
# map(lambda (k, crater): add.update({k: crater + random.gauss(0, 4)}), centers.items())
# viewer.saveData(add, "finalReferenceCatalogue")
#
# preprocessor.preprocessReferenceImage("finalReferenceCatalogue", referenceCombinations)

navigator.locateDescentImageInReferenceImage("../data/TRN/Scene1.ppm", referenceCatalogue)

