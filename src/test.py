# from matplotlib import pyplot as plt
# from scipy.cluster.hierarchy import dendrogram, linkage
# import numpy as np
# # %matplotlib inline
# np.random.seed(4711)  # for repeatability of this tutorial
# a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100,])
# b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50,])
# X = np.concatenate((a, b),)
# print X.shape  # 150 samples with 2 dimensions
# plt.scatter(X[:,0], X[:,1])
# print X
# plt.show()
from PIL import Image
from PIL import ImageDraw

import numpy as np

import shownp as viewer

from PIL import Image, ImageDraw

im = Image.open("TRN/crop1.ppm")
imagematrix = viewer.RGBToGray(np.asarray(im))
viewer.showGray(imagematrix)

# x, y =  im.size
# eX, eY = 30, 60 #Size of Bounding Box for ellipse
#
# bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
# draw = ImageDraw.Draw(im)
# draw.ellipse(bbox, fill=None, outline=128)
# del draw
#
# im.save("output.png")
# im.show()