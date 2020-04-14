from Point import Point

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