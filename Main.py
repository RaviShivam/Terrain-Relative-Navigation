import Image
import sys
from src.TerrainNavigator import Navigator
import src.CraterDetector as craterdetector

referenceAltitude = 2000

datapath = "data/"
referenceMap = "ReferenceMap.ppm"
referenceCatalogue = "finalReferenceCraterData"
defaultDescentImages = ["Scene3.ppm", "Scene4.ppm"]

args = len(sys.argv)
arguments = sys.argv

if (args is 1 or args is 0):
    navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue, datapath)
    for descentimage in defaultDescentImages:
        craterdetector.extractCratersWithImage(Image.open(datapath + "TRN/" + descentimage))
        navigator.locateDescentImageInReferenceImage(datapath + "TRN/" + descentimage)
    craterdetector.extractCratersWithImage(Image.open(datapath + "TRN/Angle1.ppm"))

else:
    navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue, datapath)
    for descentimage in arguments[1:len(arguments)]:
        navigator.locateDescentImageInReferenceImage(datapath + "TRN/" + descentimage + ".ppm")
