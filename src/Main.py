import random
from PIL import Image

import shownp as viewer
import Preprocessor as preprocessor
import src.TerrainNavigator as navigator
import CraterDetector as craterdetector
from src.Crater import Crater

referenceCatalogue = "referenceCatalogue"
referenceCombinations = "combinations"

centers = craterdetector.retrieveCraterCenterpointsAndDiameters(Image.open("../TRN/ReferenceMap.ppm"))
#
# preprocessor.preprocessReferenceImage("addfile", referenceCombinations)
add = {}
map(lambda (k, crater): add.update({k: crater + random.gauss(0, 1)}), centers.items())
viewer.saveData(add, "addfile")

# preprocessor.preprocessReferenceImage(referenceCatalogue, referenceCombinations)


navigator.locateDescentImageInReferenceImage("../TRN/Scene1.ppm")

