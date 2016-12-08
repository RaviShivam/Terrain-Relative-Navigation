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



im = Image.open("TRN/Scene1.ppm")
# imagematrix = viewer.RGBToGray(np.asarray(im))
# viewer.showGray(imagematrix)
r = 5
y = 91
x = 365
y2 = 237
x2 = 275
x3 = 258
y3 = 246
bbox =  (x - r, y - r, x + r , y + r)
bbox2 =  (x2 - r, y2 - r, x2 + r , y2 + r)
bbox3 =  (x3 - r, y3 - r, x3 + r , y3 + r)
draw = ImageDraw.Draw(im)
draw.ellipse(bbox, fill=200, outline=128)
draw.ellipse(bbox2, fill=200, outline=128)
draw.ellipse(bbox3, fill=0, outline=128)
del draw

im.save("output.png")
im.show()