import math
import random

def J_func(z):
    k = 1
    u = 0.01
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


z0 = 5
func = lambda x, y: J_func(math.sqrt(x ** 2+ y ** 2 + z0 ** 2))
print(GetDoubleIntegral(func, - 10, 10, -10, 10, 1_000_000))