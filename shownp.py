import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

def RGBToGray(rgb):
    return 255 - np.dot(rgb[..., :3], [0.299, 0.587, 0.114])

def showGray(img):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.matshow(img, cmap=matplotlib.cm.binary)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    plt.show()
