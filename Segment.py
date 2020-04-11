from Point import Point
import numpy as np

class Segment:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "[a={0}; b={1}]".format(self.a, self.b)

    def FindIntersectionPoint(self, another):
        (x, z) = get_intersect((self.a.x, self.a.z), (self.b.x, self.b.z), (another.a.x, another.a.z), (another.b.x, another.b.z))
        if x == None:
            return None
        p = Point(x = x, y = 0, z = z)
        if self.IsInArea(p) and another.IsInArea(p):
            return p
        else:
            return None
    
    def IsInArea(self, point):
        return (min(self.a.x, self.b.x) <= point.x <= max(self.a.x, self.b.x) and 
                min(self.a.y, self.b.y) <= point.y <= max(self.a.y, self.b.y) and 
                min(self.a.z, self.b.z) <= point.z <= max(self.a.z, self.b.z))

def get_intersect(a1, a2, b1, b2):
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return None
    return (x/z, y/z)