# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 17:35:38 2022

@author: jeffr
"""

import PlasmaPhysics as pp
from PlasmaPhysics.unitsystems import _c, _pi

# Notes: it is safe to work entirely within SI and make conversions from non SI/MKS to SI. Care
# must be taken when converting from other systems into a target system when in non-SI unit
# systems. When a certain system has a named unit for a physical quantity while another does not
# they do not easily convert back and forth due to different coupling factors in the unit systems.
# The standard conversion factors that we are used to from say CGS to SI are built specifically for
# conversion to SI and not vice versa.
#
# Adding additional derived units is trivial for the user story of using the global package variable
# PlasmaPhysics.units. This is just a class variable with unit conversions as attributes. A new unit
# conversion is added by adding the corresponding conversion attribute to the class. Note that this
# will only change the global variable and calls to PlasmaPhysics.set_unit_system or 
# PlasmaPhysics.unitsystems.set_unit_system will override these changes.
#
# In order to facilitate adding more persistent and consistent unit definitions from the user at
# at runtime, there really should be functionality to not only update the global definitions in 
# PlasmaPhysics.unitsystems, but also the factories for creating the units and constants
# dataclasses since they are current defined at compile time.
# 
# For permanent changes after initialization/adding the units, module level dictionary definitions of
# the units must be made within PlasmaPhysics.unitsystems. 
#
# Heaviside-Lorentz are still in works; do not use them.
# 
# Known issues: 
#
# 1) unrationalized unit systems with units that are not in other systems have a very 
# annoying 4*_pi in the conversion factor that cannot be accounted for if source system does not 
# have a dedicated unit. For example, the conversion between statC (ESU/Gauss) and V*m (SI) for 
# electric flux cannot be done at all in addition to equivalency issues. The other major example is
# in the magnetic "H" field. Conversion from 'oersted' in Gauss/EMU to SI is OK and 'oersted' 
# within Gauss/EMU is OK, but cannot convert to 'oersted' from ESU/SI nor ESU to/from anything else
#
# The best way around this is that the equations being used do not use the units themselves and
# ensure that the formula involved are written in the unit-independent manner using the 
# K1, K2, Alpha, Lambda coupling "units"
# 
# An alternative is to create "new unit names" in SI/ESU/EMU for electric flux and SI/ESU for
# magnetic H-field and incorporate the proper conversion factors, but then users would have to know
# or learn the new units and that they must use them.
#
# 2) Heaviside-Lorentz unit systems do not have named units...so conversion does not fit within the
# present paradigm. One could just generate artificial unit names, e.g. hlG for Heaviside-Lorentz
# Gaussian units and incorporate the proper conversion factors, but that is a big TODO.
#
# 3) for Gauss-eV systems (common in plasma physics), eV acts as both an energy and a temperature.
# This does not lend itself to a simple unit replacement with SI since Temperature, despite having
# mechanical dimensions, is not a mechanical unit and is instead it's own independent base unit.
# This actually leads to 2 separate definitions of the unit 'eV': 1 for energy, which is just the 
# conversion from eV to erg and 'eVt' which converts between thermal eV and Kelvin in SI or Kelvin
# from Gaussian-eV units. 'eV' is the standard derived unit, which is still derived and will change
# if say 'cm' is changed from the base unit to something else while 'eVt is the base unit, which
# will only change if switching systems with a different thermodynamic basis unit.

test = 'Gauss-eV'

if test == 'MKS':
    print('\nMKS')
    print(pp.units,"\n")
    print("Charge", pp.units.C, _c/10*pp.units.statC, 1/10*pp.units.abC)
    print("Electric Flux", pp.units.V*pp.units.m, 4*_pi/10*_c*pp.units.statC, 1/10*pp.units.abC)
    print("Current", pp.units.A, _c/10*pp.units.statA, 1/10*pp.units.Bi)
    print("Electric Potential", pp.units.V, 1e8/_c*pp.units.statV, 1e8*pp.units.abV)
    print("Electric Field", pp.units.V/pp.units.m, 1e6/_c*pp.units.statV/pp.units.cm, 1e6*pp.units.abV/pp.units.cm)
    print("Electric Displacement", pp.units.C/pp.units.m**2, 1e-5*_c*pp.units.statC/pp.units.cm**2, 1e-5*pp.units.abC/pp.units.cm**2)
    print("magnetic dipole moment", pp.units.A*pp.units.m**2, 1e3*_c*pp.units.statC*pp.units.cm**2, 1e3*pp.units.Bi*pp.units.cm**2, 1e3*pp.units.erg/pp.units.G)
    print("Bfield", pp.units.T, 1e4/_c*pp.units.statT, 1e4*pp.units.G)
    print("Hfield", pp.units.A/pp.units.m, 4*_pi*1e-3*_c*pp.units.statA/pp.units.cm, 4*_pi*1e-3*pp.units.Oe)
    print("Magnetic Flux", pp.units.Wb, 1e8/_c*pp.units.statWb, 1e8*pp.units.Mx)
    print("Permittivity", pp.constants.e0)
    print("Permeability", pp.constants.u0)
    print("Bohr magneton", pp.constants.uB)
    print("Elementary Charge", pp.constants.e)
    print("\nPrinciple Units\n")
    print(f"A={pp.units.A}\ncd={pp.units.cd}\nK={pp.units.K}\nmol={pp.units.mol}\nm={pp.units.m}\nkg={pp.units.kg}\ns={pp.units.s}\nV={pp.units.V}\nT={pp.units.T}\n")

if test == 'ESU':
    print('\nESU')
    pp.set_unit_system('ESU')
    print(pp.units,"\n")
    print("Charge", 10/_c*pp.units.C, pp.units.statC, 1/_c*pp.units.abC)
    print("Electric Flux", 10/(4*_pi*_c)*pp.units.V*pp.units.m, pp.units.statC, 1/(4*_pi*_c)*pp.units.abC)
    print("Current", 10/_c*pp.units.A, pp.units.statA, 1/_c*pp.units.Bi)
    print("Electric Potential", _c/1e8*pp.units.V, pp.units.statV, _c*pp.units.abV)
    print("Electric Field", _c/1e6*pp.units.V/pp.units.m, pp.units.statV/pp.units.cm, _c*pp.units.abV/pp.units.cm)
    print("Electric Displacement", 1e5/_c*pp.units.C/pp.units.m**2, pp.units.statC/pp.units.cm**2, 1/_c*pp.units.abC/pp.units.cm**2)
    print("magnetic dipole moment", 1/(1e3*_c)*pp.units.A*pp.units.m**2, pp.units.statC*pp.units.cm**2, 1/_c*pp.units.Bi*pp.units.cm**2, 1/_c*pp.units.erg/pp.units.G)
    print("Bfield", _c/1e4*pp.units.T, pp.units.statT, _c*pp.units.G)
    print("Hfield", 1e3/(4*_pi*_c)*pp.units.A/pp.units.m, pp.units.statA/pp.units.cm, 1/_c*pp.units.Oe)
    print("Magnetic Flux", _c/1e8*pp.units.Wb, pp.units.statWb, _c*pp.units.Mx)
    print("Permittivity", pp.constants.e0, 1.0)
    print("Permeability", pp.constants.u0, 1/pp.constants.c**2)
    print("Bohr magneton", pp.constants.uB, 2.78027800e-10)
    print("Elementary Charge", pp.constants.e, 4.80320427e-10)
    print("\nPrinciple Units\n")
    print(f"statA={pp.units.statA}\ncd={pp.units.cd}\nK={pp.units.K}\nmol={pp.units.mol}\ncm={pp.units.cm}\ng={pp.units.g}\ns={pp.units.s}\nstatV={pp.units.statV}\nstatT={pp.units.statT}\n")

if test == 'EMU':
    print('\nEMU')
    pp.set_unit_system('EMU')
    print(pp.units,"\n")
    print("Charge", 10*pp.units.C, _c*pp.units.statC, pp.units.abC)
    print("Electric Flux", 10*pp.units.V*pp.units.m, 4*_pi*_c*pp.units.statC, pp.units.abC)
    print("Current", 10*pp.units.A, _c*pp.units.statA, pp.units.Bi)
    print("Electric Potential", 1/1e8*pp.units.V, 1/_c*pp.units.statV, pp.units.abV)
    print("Electric Field", 1/1e6*pp.units.V/pp.units.m, 1/_c*pp.units.statV/pp.units.cm, pp.units.abV/pp.units.cm)
    print("Electric Displacement", 1e5*pp.units.C/pp.units.m**2, _c*pp.units.statC/pp.units.cm**2, pp.units.abC/pp.units.cm**2)
    print("magnetic dipole moment", 1/(1e3)*pp.units.A*pp.units.m**2, _c*pp.units.statC*pp.units.cm**2, pp.units.Bi*pp.units.cm**2, pp.units.erg/pp.units.G)
    print("Bfield", 1/1e4*pp.units.T, 1/_c*pp.units.statT, pp.units.G)
    print("Hfield", 1e3/(4*_pi)*pp.units.A/pp.units.m, _c*pp.units.statA/pp.units.cm, pp.units.Oe)
    print("Magnetic Flux", 1/1e8*pp.units.Wb, 1/_c*pp.units.statWb, pp.units.Mx)
    print("Permittivity", pp.constants.e0, 1/pp.constants.c**2)
    print("Permeability", pp.constants.u0, 1.0)
    print("Bohr magneton", pp.constants.uB, 9.274010078e-21)
    print("Elementary Charge", pp.constants.e, 1.602176634e-20)
    print("\nPrinciple Units\n")
    print(f"Bi={pp.units.Bi}\ncd={pp.units.cd}\nK={pp.units.K}\nmol={pp.units.mol}\ncm={pp.units.cm}\ng={pp.units.g}\ns={pp.units.s}\nabV={pp.units.statV}\nG={pp.units.G}\n")
    
if test == 'Gauss':
    print('\nGauss')
    pp.set_unit_system('Gauss')
    print(pp.units,"\n")
    print("Charge", 10/_c*pp.units.C, pp.units.statC, 1/_c*pp.units.abC)
    print("Electric Flux", 10/(4*_pi*_c)*pp.units.V*pp.units.m, pp.units.statC, 1/(4*_pi*_c)*pp.units.abC)
    print("Current", 10/_c*pp.units.A, pp.units.statA, 1/_c*pp.units.Bi)
    print("Electric Potential", _c/1e8*pp.units.V, pp.units.statV, _c*pp.units.abV)
    print("Electric Field", _c/1e6*pp.units.V/pp.units.m, pp.units.statV/pp.units.cm, _c*pp.units.abV/pp.units.cm)
    print("Electric Displacement", 1e5/_c*pp.units.C/pp.units.m**2, pp.units.statC/pp.units.cm**2, 1/_c*pp.units.abC/pp.units.cm**2)
    print("magnetic dipole moment", 1/(1e3)*pp.units.A*pp.units.m**2, _c*pp.units.statC*pp.units.cm**2, pp.units.Bi*pp.units.cm**2, pp.units.erg/pp.units.G)
    print("Bfield", 1/1e4*pp.units.T, 1/_c*pp.units.statT, pp.units.G)
    print("Hfield", 1e3/(4*_pi)*pp.units.A/pp.units.m, _c*pp.units.statA/pp.units.cm, pp.units.Oe)
    print("Magnetic Flux", 1/1e8*pp.units.Wb, 1/_c*pp.units.statWb, pp.units.Mx)
    print("Permittivity", pp.constants.e0, 1.0)
    print("Permeability", pp.constants.u0, 1.0)
    print("Bohr magneton", pp.constants.uB, 9.274010078e-21)
    print("Elementary Charge", pp.constants.e, 4.80320427e-10)
    print("\nPrinciple Units\n")
    print(f"statA={pp.units.statA}\ncd={pp.units.cd}\nK={pp.units.K}\nmol={pp.units.mol}\ncm={pp.units.cm}\ng={pp.units.g}\ns={pp.units.s}\nstatV={pp.units.statV}\nG={pp.units.G}\n")
    
if test == 'Gauss-eV':
    print('\nGauss-eV')
    pp.set_unit_system('Gauss-eV')
    print(pp.units,"\n")
    print("Charge", 10/_c*pp.units.C, pp.units.statC, 1/_c*pp.units.abC)
    print("Electric Flux", 10/(4*_pi*_c)*pp.units.V*pp.units.m, pp.units.statC, 1/(4*_pi*_c)*pp.units.abC)
    print("Current", 10/_c*pp.units.A, pp.units.statA, 1/_c*pp.units.Bi)
    print("Electric Potential", _c/1e8*pp.units.V, pp.units.statV, _c*pp.units.abV)
    print("Electric Field", _c/1e6*pp.units.V/pp.units.m, pp.units.statV/pp.units.cm, _c*pp.units.abV/pp.units.cm)
    print("Electric Displacement", 1e5/_c*pp.units.C/pp.units.m**2, pp.units.statC/pp.units.cm**2, 1/_c*pp.units.abC/pp.units.cm**2)
    print("magnetic dipole moment", 1/(1e3)*pp.units.A*pp.units.m**2, _c*pp.units.statC*pp.units.cm**2, pp.units.Bi*pp.units.cm**2, pp.units.erg/pp.units.G)
    print("Bfield", 1/1e4*pp.units.T, 1/_c*pp.units.statT, pp.units.G)
    print("Hfield", 1e3/(4*_pi)*pp.units.A/pp.units.m, _c*pp.units.statA/pp.units.cm, pp.units.Oe)
    print("Magnetic Flux", 1/1e8*pp.units.Wb, 1/_c*pp.units.statWb, pp.units.Mx)
    print("Permittivity", pp.constants.e0, 1.0)
    print("Permeability", pp.constants.u0, 1.0)
    print("Bohr magneton", pp.constants.uB, 9.274010078e-21)
    print("Elementary Charge", pp.constants.e, 4.80320427e-10)
    print("\nPrinciple Units\n")
    print(f"statA={pp.units.statA}\ncd={pp.units.cd}\neV={pp.units.eVt}\nmol={pp.units.mol}\ncm={pp.units.cm}\ng={pp.units.g}\ns={pp.units.s}\nstatV={pp.units.statV}\nG={pp.units.G}\n")

if test == 'HL':
    print('\nHeaviside-Lorentz - Testing not fully defined')
    pp.set_unit_system('H-L')
    print(pp.units)
    print("magnetic dipole moment", pp.units.A*pp.units.m**2, 1e3*_c*pp.units.statC*pp.units.cm**2, 1e3*pp.units.Bi*pp.units.cm**2, 1e3*pp.units.erg/pp.units.G)
    print("Bfield", pp.units.T, 1e4/_c*pp.units.statT, 1e4*pp.units.G)
    print("Hfield", pp.units.A/pp.units.m, 4*_pi*1e-3*_c*pp.units.statA/pp.units.cm, 4*_pi*1e-3*pp.units.Oe)
    print("Magnetic Flux", pp.units.Wb, 1e8/_c*pp.units.statWb, 1e8*pp.units.Mx)
    print("Permittivity", pp.constants.e0, 1.0)
    print("Permeability", pp.constants.u0, 1.0)
    print("Bohr magneton", pp.constants.uB, 9.274010078e-21)
    print("Elementary Charge", pp.constants.e, 4.80320427e-10)