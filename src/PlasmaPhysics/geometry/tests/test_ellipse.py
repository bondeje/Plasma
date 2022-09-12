# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 22:09:16 2022

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

NPTS = 20

plt.figure(1)
plt.clf()
npoints = 200
dtheta = 2*np.pi/npoints
theta = np.linspace(0, dtheta*npoints, npoints+1)
a, b = 2, 1
k = np.sqrt(1-min(a,b)**2/max(a,b)**2)
x, y = a*np.cos(theta), b*np.sin(theta)
plt.plot(x, y, label=f"Npts={npoints}")
npoints = 16
dtheta = 2*np.pi/npoints
theta = np.linspace(0, dtheta*npoints, npoints+1)
a, b = 2, 1
k = np.sqrt(1-min(a,b)**2/max(a,b)**2)
x, y = a*np.cos(theta), b*np.sin(theta)
plt.plot(x, y, label=f"Npts={npoints}")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(frameon=False, bbox_to_anchor=[1.05,1.25])
for i in range(npoints):
    plt.plot([0, a*np.cos(theta[i])], [0, b*np.sin(theta[i])], 'k')
ind = 1
#plt.plot([0, np.cos(theta[ind]+dtheta/2)*np.cos(dtheta/2)], [0, np.sin(theta[ind]+dtheta/2)*np.cos(dtheta/2)], 'k:')
plt.gca().set_aspect(1)

plt.figure(2)
plt.clf()
npoints = 200
dtheta = 2*np.pi/npoints
theta = np.linspace(0, dtheta*npoints, npoints+1)
a, b = 2, 1
k = np.sqrt(1-min(a,b)**2/max(a,b)**2)
x, y = a*np.cos(theta), b*np.sin(theta)
plt.plot(x, y, label=f"Npts={npoints}")
npoints = 16
l = npoints//4
a, b = 2, 1
k = np.sqrt(1-min(a,b)**2/max(a,b)**2)
theta = [0]
interval = ellipe(k)/l
nexttheta = partial(lambda x, y, e: (ellipeinc(x, e)-ellipeinc(y,e)-interval)**2, e=k)
for i in range(l-1):
    res = root(partial(nexttheta, y=theta[-1]), theta[-1] + np.pi/(2*l), tol=np.pi/(50*npoints))
    theta.append(res.x[0])
    print(ellipeinc(theta[-1],k)-ellipeinc(theta[-2],k))
theta.append(np.pi/2)
nexttheta = partial(lambda x, y, e: (ellipeinc(np.pi-y,e)-ellipeinc(np.pi-x, e)-interval)**2, e=k)
for i in range(l-1):
    res = root(partial(nexttheta, y=theta[-1]), theta[-1] + np.pi/(2*l), tol=np.pi/(50*npoints))
    theta.append(res.x[0])
    print(ellipeinc(np.pi-theta[-2],k)-ellipeinc(np.pi-theta[-1],k))
i = 0
while i < 2*l:
    theta.append(theta[i]-np.pi)
    i += 1
theta.sort()
theta.append(theta[0]+2*np.pi)
theta = np.array(theta)
r = np.sqrt(a**2*np.cos(theta)**2 + b**2*np.sin(theta)**2)
l = np.sqrt(r[:-1]**2 + r[1:]**2 - 2*r[:-1]*r[1:]*np.cos(theta[1:]-theta[:-1]))
x, y = a*np.cos(theta), b*np.sin(theta)
plt.plot(x, y, label=f"Npts={npoints}, equal arc length")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(frameon=False, bbox_to_anchor=[1.05,1.25])
for i in range(npoints):
    plt.plot([0, a*np.cos(theta[i])], [0, b*np.sin(theta[i])], 'k')
plt.gca().set_aspect(1)
print(l)