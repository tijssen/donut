# donut.py
# Copyright (C) 2021, 2022 Luuk Tijssen
# License CC0-1.0

import sys
from scipy.spatial.transform import Rotation as R
import numpy as np

height, width = 22, 80
larger, smallr = 2.0, 1.0
ntheta, nphi = 200, 100
k1, k2 = 0.2*width, 5.0
light_norm = 2**(-0.5)*np.array([0.0, 1.0, -1.0])
chars = ".,-~:;=!*#$@"

def phi_revolution(pos=None, num=nphi):
    if pos is None:
        pos = np.array([1.0, 0.0, 0.0])
    phi = np.pi*np.linspace(-1.0, 1.0, num)
    zeros = np.zeros_like(phi)
    r = R.from_rotvec(np.array([zeros, phi, zeros]).T)
    pos = np.matmul(pos, r.as_matrix())
    return pos

def theta_revolution(pos=None, num=ntheta):
    if pos is None:
        pos = phi_revolution()
    theta = np.pi*np.linspace(-1.0, 1.0, num)
    zeros = np.zeros_like(theta)
    r = R.from_rotvec(np.array([zeros, zeros, theta]).T)
    pos = np.matmul(pos, r.as_matrix())
    pos = np.reshape(pos, [-1, 3])
    return pos

def generate_position():
    pos = phi_revolution()
    pos = np.array([larger, 0.0, 0.0]) + smallr*pos
    pos = theta_revolution(pos)
    return pos

def generate_normal():
    return theta_revolution()

# ASCII backend
POS = generate_position()
NORM = generate_normal()

def update(i):
    aa, bb = 0.04*i, 0.02*i
    ra = R.from_rotvec([aa,  0.0, 0.0]).as_matrix()
    rb = R.from_rotvec([0.0, 0.0, bb ]).as_matrix()
    pos = np.copy(POS)
    pos = np.matmul(pos, ra)
    pos = np.matmul(pos, rb)
    norm = np.copy(NORM)
    norm = np.matmul(norm, ra)
    norm = np.matmul(norm, rb)
    zbuffer = np.zeros([height, width]) # 1/z = 0.0 -> z = inf
    screen = np.resize(" ", [height, width])

    x, y, z = pos.T
    light = np.dot(norm, light_norm)
    z = k2 + z
    ooz = 1.0/z
    x_ = (width/2 + 2*k1*ooz*x).astype(int)
    y_ = (height/2 - k1*ooz*y).astype(int)
    mask = (0 <= x_) & (x_ < width) & (0 <= y_) & (y_ < height)
    x_, y_, ooz, light = x_[mask], y_[mask], ooz[mask], light[mask]
    for x, y, ooz, l in zip(x_, y_, ooz, light):
        if ooz > zbuffer[y, x]:
            zbuffer[y, x] = ooz
            screen[y, x] = chars[max(0, int(l*len(chars)))]

    print("\x1b[H")
    np.savetxt(sys.stdout.buffer, screen, fmt="%s", delimiter="")

print(height*"\n")
i = 0

while True:
    update(i)
    i += 1

"""
# Matplotlib backend
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

light_norm = 2**(-0.5)*np.array([0.0, -1.0, 1.0])

POS = generate_position()
NORM = generate_normal()


def update(i):
    aa, bb = 0.04*i, 0.02*i
    ra = R.from_rotvec([aa,  0.0, 0.0]).as_matrix()
    rb = R.from_rotvec([0.0, 0.0, bb ]).as_matrix()
    pos = np.copy(POS)
    pos = np.matmul(pos, ra)
    pos = np.matmul(pos, rb)
    norm = np.copy(NORM)
    norm = np.matmul(norm, ra)
    norm = np.matmul(norm, rb)
    x, y, z = pos.T
    light = np.dot(norm, light_norm)
    light[light < 0.0] = 0.0
    ax.cla()
    ax.scatter(x, y, z, c=light, marker=".", s=1.0)
    lim = [-3.0, 3.0]
    ax.set(xlim=lim, ylim=lim, zlim=lim)
    ax.set(xlabel="x", ylabel="y", zlabel="z")
    ax.axis("off")

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.set_box_aspect([1.0, 1.0, 1.0])
plt.set_cmap("Greys_r")
ax.set_facecolor("black")
ani = FuncAnimation(fig=fig, func=update, frames=10000, interval=1)
plt.show()
"""
