import os

os.chdir(r"C:\SharedDocs\Python\Plasma\src")

from PlasmaPhysics import geometry
from PlasmaPhysics import utils
import numpy as np
import matplotlib.pyplot as plt

NPTS = 20

plt.figure(1)
plt.clf()
ax = plt.gcf().add_subplot(projection='3d')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

a = geometry.circle(1)
a.draw(ax)

b = geometry.circle(2, fill=True)
b.draw(ax)

c = geometry.circle(1, location = [0, 0, 1], npoints = NPTS)
c.draw(ax)

d = geometry.circle(1, location = [0, 1, 0], orientation=[0, 1, 0], npoints = NPTS)
d.draw(ax)

e = geometry.circle(1, location = [0, 0, -1], orientation=[1, 0, 0], npoints = NPTS)
e.draw(ax)

f = geometry.circle(np.sqrt(2), location = [1, 0, -1], orientation=[1/np.sqrt(2), 0, 1/np.sqrt(2)], npoints = NPTS)
f.draw(ax)

Ntest = 80
circums = np.zeros((Ntest,Ntest))
circums_calc = np.zeros((Ntest,Ntest))
npts = [int(80/Ntest*it+4) for it in range(Ntest)]
radius = np.array([.1 + 4/Ntest*it for it in range(Ntest)])
for i in range(Ntest):
    for j in range(Ntest):
        circums[i,j] = 2*np.pi*radius[i]
        g = geometry.circle(radius[i], npoints=npts[j])
        circums_calc[i,j] = g.length()
        
plt.figure(2)
plt.clf()
ax = plt.gcf().add_subplot(projection='3d')
ax.contourf(*np.meshgrid(npts, radius), (circums_calc-circums)/circums)
ax.set_xlabel("number of points")
ax.set_ylabel("radius")

plt.figure(3)
plt.clf()
ind = 0
plt.plot(npts, circums[ind,:], label=f'true circumference, radius={radius[ind]}')
plt.plot(npts, circums_calc[ind,:], label=f'calculated circumference, radius={radius[ind]}')
ind = Ntest-1
plt.plot(npts, circums[ind,:], label=f'true circumference, radius={radius[ind]}')
plt.plot(npts, circums_calc[ind,:], label=f'calculated circumference, radius={radius[ind]}')
plt.xlabel("number of points")
plt.ylabel("Circumference")
plt.legend()

plt.figure(4)
plt.clf()
ind = 0
plt.plot(npts, (circums_calc[ind,:]-circums[ind,:])/circums[ind,:],":", label=f'rel. error, radius={radius[ind]}')
ind = Ntest-1
plt.plot(npts, (circums_calc[ind,:]-circums[ind,:])/circums[ind,:],"-", label=f'rel. error, radius={radius[ind]}')
npts = np.array(npts)
err = -np.pi**2/6/npts**2*(1-1/20*np.pi**2/npts**2)
plt.plot(npts, err, '--', label="model")
plt.xlabel("number of points")
plt.ylabel("Circumference")
plt.legend()

#%% for documents

plt.figure(5)
plt.clf()
npoints = 100
dtheta = 2*np.pi/npoints
theta = np.linspace(0, dtheta*npoints, npoints+1)
x, y = np.cos(theta), np.sin(theta)
plt.plot(x, y, label=f"Npts={npoints}")
npoints = 10
dtheta = 2*np.pi/npoints
theta = np.linspace(0, dtheta*npoints, npoints+1)
x, y = np.cos(theta), np.sin(theta)
plt.plot(x, y, label=f"Npts={npoints}")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(frameon=False, bbox_to_anchor=[1.35,.95])
for i in range(npoints):
    plt.plot([0, np.cos(theta[i])], [0, np.sin(theta[i])], 'k')
ind = 1
plt.plot([0, np.cos(theta[ind]+dtheta/2)*np.cos(dtheta/2)], [0, np.sin(theta[ind]+dtheta/2)*np.cos(dtheta/2)], 'k:')
plt.gca().set_aspect(1)
