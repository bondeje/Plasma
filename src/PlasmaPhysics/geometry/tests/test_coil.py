# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 20:52:22 2022

@author: jeffr
"""

import os

os.chdir(r"C:\SharedDocs\Python\Plasma\src")

from PlasmaPhysics import geometry
from PlasmaPhysics import utils
import numpy as np
from scipy.special import ellipe, ellipeinc
from scipy.optimize import root
from functools import partial
import matplotlib.pyplot as plt

NPTS = 150

plt.figure(1)
plt.clf()
ax = plt.gcf().add_subplot(projection='3d')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

a = geometry.coil(4, .5, 16, npoints=NPTS)
a.draw(ax)

xd = ax.get_xlim()[1] - ax.get_xlim()[0]
yd = ax.get_ylim()[1] - ax.get_ylim()[0]
zd = ax.get_zlim()[1] - ax.get_zlim()[0]
ax.set_box_aspect((xd, yd, zd))

plt.figure(2)
plt.clf()
ax = plt.gcf().add_subplot(projection='3d')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

a = geometry.coil(4, .5, 16, npoints=NPTS)
a.rotate(np.array([1,0,0])*np.pi/2)
a.draw(ax)

xd = ax.get_xlim()[1] - ax.get_xlim()[0]
yd = ax.get_ylim()[1] - ax.get_ylim()[0]
zd = ax.get_zlim()[1] - ax.get_zlim()[0]
ax.set_box_aspect((xd, yd, zd))

plt.figure(3)
plt.clf()
ax = plt.gcf().add_subplot(projection='3d')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

a = geometry.coil(4, .5, 32, npoints=NPTS)
a.rotate(np.array([0,1,0])*np.pi*3/4)
a.draw(ax)

xd = ax.get_xlim()[1] - ax.get_xlim()[0]
yd = ax.get_ylim()[1] - ax.get_ylim()[0]
zd = ax.get_zlim()[1] - ax.get_zlim()[0]
ax.set_box_aspect((xd, yd, zd))