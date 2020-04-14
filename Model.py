from Point import Point
from Segment import Segment

X_MIN = -10
X_MAX = 20
Y_MIN = 0
Y_MAX = 10

def GetZ(x):
    if x < 0:
        return 0
    if x < 7:
        return 4
    if x < 10:
        return 7
    if x < 15:
        return 0
    return 10

def GetSegments():
    keyPoints = [
        Point(x = X_MIN, z = 0),
        Point(x = 0, z = 0),
        Point(x = 0, z = 4),
        Point(x = 7, z = 4),
        Point(x = 7, z = 7),
        Point(x = 10, z = 7),
        Point(x = 10, z = 0),
        Point(x = 15, z = 0),
        Point(x = 15, z = 10),
        Point(x = 25, z = 10)
    ]    
    prev = None
    for keyPoint in keyPoints:
        if prev != None:
            yield Segment(prev.copy(), keyPoint.copy())
        prev = keyPoint