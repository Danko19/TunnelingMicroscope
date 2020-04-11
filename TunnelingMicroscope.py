import math
import random
import numpy
import Model
from Point import Point
from Segment import Segment

def J_func(z, u):
    k = 1
    Ef = 5.71
    fi = 4.5
    s1 = 3 / (k * fi)
    s2 = z * (1 - 23 / (3 * fi * k * z + 10 - 2 * u * k * z)) + s1
    fi_z = fi - (u * (s1 + s2)) / (2 * z) - 2.86 / (k * (s2 - s1)) * math.log((s2 * (z - s1)) / (s1 * (z - s2)))
    return 1620 * u * Ef * math.exp(-1.025 * z * math.sqrt(fi_z))

def GetDoubleIntegral(func, x1, x2, y1, y2, n):
    s = 0
    for i in range(n):
        x = random.uniform(x1, x2)
        y = random.uniform(y1, y2)
        s += func(x,y)
    return s * (x2 - x1) * ( y2 - y1) / n
    
segments = [x for x in Model.GetSegments()]

z0 = 5
u = 0.01
func = lambda x, y: J_func(math.sqrt(x ** 2+ y ** 2 + z0 ** 2), u)
I_et = GetDoubleIntegral(func, - 10, 10, -10, 10, 100_000)

y = 0
for x in map(lambda x: round(x,1), numpy.arange(Model.X_MIN, Model.X_MAX + 0.1, 0.1)):
    def I_z(z):
        p = Point(x = x, y = y, z = z)
        def dist_func(model_x, model_y):
            model_z = Model.GetZ(model_x)
            model_p = Point(model_x, model_y, model_z)
            touch_p = model_p.copy()
            return p.GetDistance(touch_p)
            s = Segment(p, model_p)
            for segment in segments:
                next_p = s.FindIntersectionPoint(segment)
                if next_p == None:
                    continue
                if x - touch_p.x != 0:
                    next_p.y = model_y * abs(x - next_p.x) / abs(x - touch_p.x)
                else:
                    next_p.y = model_y * abs(z - next_p.z) / abs(z - touch_p.z)
                if next_p != None and p.GetDistance(next_p) < p.GetDistance(touch_p):
                    touch_p = next_p
            return p.GetDistance(touch_p)
            
        func = lambda x_0, y_0: J_func(dist_func(x_0, y_0), u)
        return GetDoubleIntegral(func, x - 10, x + 10, -10, 10, 10_000)

    print(x)
    print(I_z(5))
    print(I_z(6))


def NewtonMethod(func, x1, x2, e):
    s = 1