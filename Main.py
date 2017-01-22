import sys
from src.TerrainNavigator import Navigator

referenceAltitude = 2000

datapath = "../data/"
referenceMap = "ReferenceMap.ppm"
referenceCatalogue = "finalReferenceCraterData"
defaultDescentImages = ["Scene1.ppm", "Scene2.ppm", "Scene3.ppm", "Scene4.ppm"]

args = len(sys.argv)
arguments = sys.argv

if (args is 1 or args is 0):
    navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue, datapath)
    for descentimage in defaultDescentImages:
        navigator.locateDescentImageInReferenceImage(datapath + "TRN/" + descentimage)
else:
    navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue, datapath)
    for descentimage in arguments[1:len(arguments)]:
        navigator.locateDescentImageInReferenceImage(datapath + "TRN/" + descentimage + ".ppm")
