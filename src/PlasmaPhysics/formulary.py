import numpy as np
from . import unitsystems as us

# globals used as default values
ELECTRON = 'e'
PROTON = 'p'

# defaults correspond to electron
def plasma_frequency(density, mass, charge=-1, angular=True):
    factor = 1.0 if angular else 1/(2*us._pi)
    #if mass == ELECTRON:
    #    mass = us._constants.me
    return (factor*abs(charge)*us._constants.e*(us._units.Lambda/(us._constants.e0*mass))**.5)*np.sqrt(density)

# defaults correspond to electron
def gyro_frequency(B, mass, charge=-1, angular=True):
    factor = 1.0 if angular else 1/(2*us._pi)
    #if mass == ELECTRON:
    #    mass = us._constants.me
    return (factor*abs(charge)*us._constants.e/(mass*us._units.Alpha))*B

# defaults correspond to electron
# TODO check if wavenumber is 2*pi/lambda or 1/lambda
#def trapping_rate(charge=-1); need to verify equation; the NRL one looks dimensionally inconsistent
# allocating an 'as-yet-to-be-defined' argument 'dist' to allow for non-Maxwellian distribution thermal velocities to use the same signature
def thermal_velocity(T, mass, dist='Maxwellian'):
    #if mass == ELECTRON:
    #    mass = us._constants.me
    return (us._constants.kB/mass)**.5*T**.5

# allocating an 'as-yet-to-be-defined' argument 'dist' to allow for non-Maxwellian distribution thermal velocities to use the same signature
def sound_velocity(Te, mass, charge=1, gamma=5.0/3, dist='Maxwellian'):
    #if mass == PROTON:
    #    mass = us._constants.mp
    return (abs(charge)*gamma*us._constants.kB/mass)**.5*Te**.5

def gyro_radius(T, B, mass, charge=-1):
    #if mass == ELECTRON:
    #    mass = us._constants.me
    return thermal_velocity(T, mass)/gyro_frequency(B, mass, charge, angular=True)

def inertial_length(density, mass, charge=-1):
    #if mass == ELECTRON:
    #    mass = us._constants.me
    return us._constants.c/plasma_frequency(density, mass, charge, angular=True)

# TODO: modify to allow calculation of the ion debye length though that's not very meaningful
def Debye_length(density, T, mass, charge=-1, gamma=5./3, dist='Maxwellian'):
    #if mass == ELECTRON:
    #    mass = us._constants.me
    # not sure that it necessarily matters, but this is likely not the most efficient calculation of this quantity
    return thermal_velocity(T, mass, dist)/plasma_frequency(density, mass, charge, angular=True)

def Alfven_velocity(B, density, mass):
    #if mass == PROTON:
    #    mass = us._constants.mp
    return 1/(us._units.Lambda*us._constants.u0*mass)**.5*B/density**.5

def Bohm_diffusion(B, T):
    return (us._units.Alpha*us._constants.kB/us._constants.e/16)*T/B