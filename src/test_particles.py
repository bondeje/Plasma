# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 11:37:43 2022

@author: jeffr
"""

import PlasmaPhysics as pp
import numpy as np
from PlasmaPhysics import unitsystems as us
from PlasmaPhysics import particles
from PlasmaPhysics.dbutils import NIST

dt = 1.5

electron = particles.Particle(name="electron", position=np.array([0.0, 0.0, 0.0]), momentum=us._constants.me*np.array([1.0, 0.0, 0.0]), mass=us._constants.me)

electron.move(dposition=electron.momentum*dt/electron.mass)
print(f"electron position: {electron.position}, electron velocity: {electron.momentum/electron.mass}")
electron.move(dmomentum=electron.mass*np.array([0, 1.3, 0]))
print(f"electron position: {electron.position}, electron velocity: {electron.momentum/electron.mass}")

Ar2 = particles.Atom(states='Ar2+', position=[0,0,1], momentum = np.array([0,us._units.Da*39.946, 0]), mass = 39.946*us._units.Da)
print(Ar2.name, Ar2.mass, Ar2.charge, Ar2.state, Ar2.position, Ar2.momentum)

XeIII = particles.Atom(charge=2, mass=us._units.Da*131.293)
print(XeIII.name, XeIII.mass, XeIII.charge, XeIII.state, XeIII.position, XeIII.momentum)
