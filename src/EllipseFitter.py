import numpy as np

import math
import random
import scipy.cluster.hierarchy as hcluster
from PIL import Image
from PIL import ImageDraw
import matplotlib.pyplot as plt

import shownp as viewer


def rotatePointAround(rightpoint, middlepoint):
    print "rightpoint= {}, middlepoint= {}".format(rightpoint, middlepoint)
    rotationpoint = np.array([rightpoint[0] - middlepoint[0], rightpoint[1]-middlepoint[1]])
    theta = math.radians(90)
    c, s = np.cos(theta), np.sin(theta)
    rotationMatrix = np.matrix('{} {}; {} {}'.format(c, -s, s, c))
    rotationpoint = np.dot(rotationMatrix, rotationpoint)
    rotationpoint = rotationpoint.tolist()[0]
    rotationpoint = [rotationpoint[0]+middlepoint[0], rotationpoint[1]+middlepoint[1]]
    return rotationpoint

def retrieveSemiMinorAxis(fartestpoints, middlepoint, draw):
    rightpoint =[]
    if (fartestpoints[0][0] > fartestpoints[1][0]):
        rightpoint = fartestpoints[0]
    else:
        rightpoint = fartestpoints[1]
    rotatedpoint = rotatePointAround(rightpoint, middlepoint)
    viewer.drawpoint(draw, middlepoint, 6)
    # viewer.drawpoint(draw, (rotatedpoint[1], rotatedpoint[0]), 6)


def drawFoundCraters(sortedclusters, imagematrix, im):
    draw = ImageDraw.Draw(im)
    # edges = []
    for (k, v) in sortedclusters.items():
        edgecluster = viewer.findEdges(v, imagematrix) #Retrieves map of edgepoints in each cluster.
        # map(lambda x: viewer.drawpoint(draw, (x[1], x[0]), 6), v)
        distance, fartestpoints = viewer.searchForFartestPoint(edgecluster) #Search for fartestpoint in cluster for diameter determination.
        # viewer.drawpoint(draw, (fartestpoints[0][1],fartestpoints[0][0]), 6)
        # viewer.drawpoint(draw, fartestpoints[0], 6)
        diameter = 1.35 * distance
        a = diameter / 2
        x, y = viewer.calculateMiddlePoint(diameter, fartestpoints)
        x = x + random.gauss(0, 2)
        y = y + random.gauss(0, 2)
        b = retrieveSemiMinorAxis(fartestpoints, (x,y), draw)
        bbox = (x - a, y - a, x + a, y + a)
        # im = viewer.draw_ellipse(im, bbox, width=4) #Thick bounds
        # draw.ellipse(bbox, fill=None, outline=400) #less thick bounds

    # viewer.plotClusters(edges)
    # del draw
    im.save("output.png")
    im.show()


