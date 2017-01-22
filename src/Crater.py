

"""
Data structure for storing data on a certain crater.
"""
import numpy as np
class Crater:
    def __init__(self, id, centerpoint, diameter):
        self.id = id
        self.centerpoint = centerpoint
        self.diameter = diameter

    def __str__(self):
        return "Crater: <centerpoint= {}, diameter= {}>".format(self.centerpoint, self.diameter)

    def __repr__(self):
        return self.__str__()

class ClusterCrater:
    def __init__(self, id, points):
        self.id = id
        self.points = points
        centerpoint = [0.0, 0.0]
        for point in points:
            centerpoint[0] = centerpoint[0] + point[0]
            centerpoint[1] = centerpoint[1] + point[1]
        self.centerpoint = map(lambda x: x/len(points), centerpoint)

    def distanceTo(self, secondcluster):
        dist = np.linalg.norm(np.array(self.centerpoint) - np.array(secondcluster.centerpoint))
        return dist
