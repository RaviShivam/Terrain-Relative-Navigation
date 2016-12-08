import numpy as np
import os, pickle
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

def searchForFartestPoint(points):
    maxdis = 0;
    farpoints = [points[0],points[1]]
    for k in range(0,len(points)):
        for l in range(k,len(points)):
            i, j = points[k], points[l]
            newdis = np.sqrt(np.square(i[0]-j[0]) + np.square(i[1]-j[1]))
            if (newdis > maxdis):
                maxdis = newdis
                farpoints = [i,j]
    return (maxdis, farpoints)

def findEdges(points, imagematrix):
    edges = []
    for point in points:
        x = point[0]
        y = point[1]
        if (imagematrix[x+1,y]==255 or
            imagematrix[x,y+1]==255 or
            imagematrix[x-1,y]==255 or
            imagematrix[x,y-1]==255):
            edges.append([x,y])
    return edges

def RGBToGray(rgb):
    return 255 - np.dot(rgb[..., :3], [0.299, 0.587, 0.114])

def showGray(img):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.matshow(img, cmap=matplotlib.cm.binary)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    plt.show()


def saveCombinations(allCombinations, file):
    dir_path = os.path.join(os.curdir, "data")
    combinationsfile = os.path.join(dir_path, file)
    combinationdata = pickle.dumps(allCombinations, protocol=0)
    f = open(combinationsfile, "wb")
    f.write(combinationdata)
    f.close()

def readCombinations(file):
    f = open(os.path.join(os.curdir, "data", file), "rb")
    layers_data = f.read()
    return pickle.loads(layers_data)

