from PIL import Image

import shownp as viewer
import Preprocessor as preprocessor
import src.TerrainNavigator as navigator
from src.Crater import Crater

referenceCatalogue = "referenceCatalogue"
referenceCombinations = "combinations"

preprocessor.preprocessReferenceImage(referenceCatalogue, referenceCombinations)


# navigator.locateDescentImageInReferenceImage("../TRN/Scene1.ppm")

