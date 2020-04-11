import math

class Point:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "(x={0}; y={1}; z={2})".format(self.x, self.y, self.z)

    def GetDistance(self, another):
        dist = 0
        dist += (self.x - another.x) ** 2
        dist += (self.y - another.y) ** 2
        dist += (self.z - another.z) ** 2
        return math.sqrt(dist)

    def copy(self):
        return Point(self.x, self.y, self.z)