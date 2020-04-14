import math
import random
import numpy
import Model
import matplotlib.pyplot as plt
import numpy as np
from Point import Point
from Segment import Segment

integral_inters = 1_000
integral_d = 5

rnds = []
for i in range(integral_inters * 2):
    rnds.append(random.uniform(-integral_d, integral_d))

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
        x = rnds[i * 2] + (x1 + integral_d)
        y = rnds[i * 2 + 1] + (y1 + integral_d)
        s += func(x,y)
    return s * (x2 - x1) * ( y2 - y1) / n

def NewtonMethod(func, z1, z2, e):
    stop = False
    f1 = func(z1)
    f2 = func(z2)
    while not stop and abs(f2 - f1) != 0:
        z_next = z2 - f2 * (z2 - z1) / (f2 - f1)
        z1 = z2
        z2 = z_next
        f1 = f2
        f2 = func(z_next)
        stop = abs(f2 - f1) <= e
    return (f2, z2)

def prepareGraph(methodName, z0):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Major ticks every 20, minor ticks every 5
    major_ticks = np.arange(Model.X_MIN, Model.X_MAX + 1, 10)
    major_ticksy = np.arange(Model.X_MIN, Model.X_MAX + 1, 5)
    minor_ticks = np.arange(Model.X_MIN, Model.X_MAX + z0 + 1, 1)

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticksy)
    ax.set_yticks(minor_ticks, minor=True)

    # And a corresponding grid
    ax.grid(which='both')

    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    plt.xlim(Model.X_MIN, Model.X_MAX)
    plt.ylim(Model.Y_MIN, Model.Y_MAX + z0 + 1)
    plt.title(methodName)

Z_d = [5, 7, 10, 15]
U_d = [0.01, 0.1]
data=[]
for Z in Z_d:
    for U in U_d:
        data.append((Z, U))

res_global = []

for (z0, u) in data:
    results = []
    res_global.append(("z0={0}; u={1}".format(z0, u), results))
    func = lambda x, y: J_func(math.sqrt(x ** 2+ y ** 2 + z0 ** 2), u)
    I_et = GetDoubleIntegral(func, -integral_d, integral_d, -integral_d, integral_d, integral_inters)

    y = 0
    test = True
    for x in map(lambda x: round(x,1), numpy.arange(Model.X_MIN, Model.X_MAX + 0.1, 0.1)):
        def I_z(z):
            p = Point(x = x, y = y, z = z)
            def dist_func(model_x, model_y):
                model_z = Model.GetZ(model_x)
                model_p = Point(model_x, model_y, model_z)
                touch_p = model_p.copy()
                return p.GetDistance(touch_p)
                
            func = lambda x_0, y_0: J_func(dist_func(x_0, y_0), u)
            return GetDoubleIntegral(func, x - integral_d, x + integral_d, -integral_d, integral_d, integral_inters)

        if test:
            I = I_z(z0)
            if I > (I_et * 1.05):
                test = False
                results.append((x, z0 + 0.5))
            else:
                results.append((x, z0))
        else:
            z1 = results[-2][1]
            z2 = results[-1][1]
            (_, z_next) = NewtonMethod(lambda z: I_z(z) - I_et, z1, z2, I_et * 0.05)
            print("x={}; z={}".format(x, z_next))
            results.append((x, z_next))

    prepareGraph("Профилограмма (z0={0}, u={1})".format(z0, u), z0)
    xs =  [t for t in map(lambda t: t[0], results)]
    zs =  [t for t in map(lambda t: t[1], results)]
    ms =  [Model.GetZ(t) for t in xs]
    plt.plot(xs, zs)
    plt.plot(xs, ms)
    plt.savefig("D:\\profs\\Профилограмма z0={0} u={1}.png".format(z0, u))
    plt.show()