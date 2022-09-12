# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 17:35:38 2022

@author: jeffr
"""

from PlasmaPhysics import formulary as f
from PlasmaPhysics import unitsystems as us

# default units in SI
table = [[    "name                  ", "MKS", "ESU", "EMU", "Gauss", "Gauss-eV"]]
wpe = 5.64e4*1e12**.5
table.append(["w_pe      @1e18m**-3  ", round(f.plasma_frequency(1e18*us._units.m**-3, mass=us._constants.me)/wpe, 3)] + [None]*4)
wpi = 1.32e3*2/39.946**.5*1e13**.5
table.append(["w_pi Ar++ @1e19m**-3  ", round(f.plasma_frequency(1e19*us._units.m**-3, mass=6.6335209e-26*us._units.kg, charge=2)/wpi, 3)] + [None]*4)
wce = 1.76e7*750
table.append(["w_ce      @750G       ", round(f.gyro_frequency(750*us._units.G, mass=us._constants.me)/wce, 3)] + [None]*4)
wci = 9.58e3*2/39.946*625
table.append(["w_ci Ar++ @625G       ", round(f.gyro_frequency(625*us._units.G, mass=6.6335209e-26*us._units.kg, charge=2)/wci, 3)] + [None]*4)
vte = 4.19e7*8.5**.5 # in cm/s
table.append(["v_te      @8.5eV      ", round(f.thermal_velocity(8.5*us._units.eVt, us._constants.me)/(vte*us._units.cm/us._units.s), 3)] + [None]*4) # 
vti = 9.79e5*12.3**.5/39.946**.5 # in cm/s
table.append(["v_te Ar++ @12.3eV     ", round(f.thermal_velocity(12.3*us._units.eVt, mass=6.6335209e-26*us._units.kg)/(vti*us._units.cm/us._units.s), 3)] + [None]*4) # 
Cs = 9.79e5*(5/3.0*2*9.7/39.946)**.5
table.append(["c_s Ar++ @9.7eV y=5/3 ", round(f.sound_velocity(9.7*us._units.eVt, mass=6.6335209e-26*us._units.kg, charge=2)/(Cs*us._units.cm/us._units.s), 3)] + [None]*4)
VA = 2.18e11*130/(1e13*39.946)**.5
table.append(["V_A Ar++ @130G 1e13ccm", round(f.Alfven_velocity(130*us._units.G, 1e13*us._units.cm**-3, mass=6.6335209e-26*us._units.kg)/(VA*us._units.cm/us._units.s), 3)] + [None]*4)
BD = 6.25e6*14.6/1230
table.append(["D_Bohm @1230G 14.6eV  ", round(f.Bohm_diffusion(1230*us._units.G, 14.6*us._units.eVt)/(BD*us._units.cm**2/us._units.s), 3)] + [None]*4)

us.set_unit_system('ESU')

table[1][2] = round(f.plasma_frequency(1e18*us._units.m**-3, mass=us._constants.me)/wpe, 3)
table[2][2] = round(f.plasma_frequency(1e19*us._units.m**-3, mass=6.6335209e-26*us._units.kg, charge=2)/wpi, 3)
table[3][2] = round(f.gyro_frequency(750*us._units.G, mass=us._constants.me)/wce, 3)
table[4][2] = round(f.gyro_frequency(625*us._units.G, mass=6.6335209e-26*us._units.kg, charge=2)/wci, 3)
table[5][2] = round(f.thermal_velocity(8.5*us._units.eVt, mass=us._constants.me)/(vte*us._units.cm/us._units.s), 3)
table[6][2] = round(f.thermal_velocity(12.3*us._units.eVt, mass=6.6335209e-26*us._units.kg)/(vti*us._units.cm/us._units.s), 3)
table[7][2] = round(f.sound_velocity(9.7*us._units.eVt, mass=6.6335209e-26*us._units.kg, charge=2)/(Cs*us._units.cm/us._units.s), 3)
table[8][2] = round(f.Alfven_velocity(130*us._units.G, 1e13*us._units.cm**-3, mass=6.6335209e-26*us._units.kg)/(VA*us._units.cm/us._units.s), 3)
table[9][2] = round(f.Bohm_diffusion(1230*us._units.G, 14.6*us._units.eVt)/(BD*us._units.cm**2/us._units.s), 3)

us.set_unit_system('EMU')

table[1][3] = round(f.plasma_frequency(1e18*us._units.m**-3, mass=us._constants.me)/wpe, 3)
table[2][3] = round(f.plasma_frequency(1e19*us._units.m**-3, mass=6.6335209e-26*us._units.kg, charge=2)/wpi, 3)
table[3][3] = round(f.gyro_frequency(750*us._units.G, mass=us._constants.me)/wce, 3)
table[4][3] = round(f.gyro_frequency(625*us._units.G, mass=6.6335209e-26*us._units.kg, charge=2)/wci, 3)
table[5][3] = round(f.thermal_velocity(8.5*us._units.eVt, mass=us._constants.me)/(vte*us._units.cm/us._units.s), 3)
table[6][3] = round(f.thermal_velocity(12.3*us._units.eVt, mass=6.6335209e-26*us._units.kg)/(vti*us._units.cm/us._units.s), 3)
table[7][3] = round(f.sound_velocity(9.7*us._units.eVt, mass=6.6335209e-26*us._units.kg, charge=2)/(Cs*us._units.cm/us._units.s), 3)
table[8][3] = round(f.Alfven_velocity(130*us._units.G, 1e13*us._units.cm**-3, mass=6.6335209e-26*us._units.kg)/(VA*us._units.cm/us._units.s), 3)
table[9][3] = round(f.Bohm_diffusion(1230*us._units.G, 14.6*us._units.eVt)/(BD*us._units.cm**2/us._units.s), 3)

us.set_unit_system('Gauss')

table[1][4] = round(f.plasma_frequency(1e18*us._units.m**-3, mass=us._constants.me)/wpe, 3)
table[2][4] = round(f.plasma_frequency(1e19*us._units.m**-3, mass=6.6335209e-26*us._units.kg, charge=2)/wpi, 3)
table[3][4] = round(f.gyro_frequency(750*us._units.G, mass=us._constants.me)/wce, 3)
table[4][4] = round(f.gyro_frequency(625*us._units.G, mass=6.6335209e-26*us._units.kg, charge=2)/wci, 3)
table[5][4] = round(f.thermal_velocity(8.5*us._units.eVt, mass=us._constants.me)/(vte*us._units.cm/us._units.s), 3)
table[6][4] = round(f.thermal_velocity(12.3*us._units.eVt, mass=6.6335209e-26*us._units.kg)/(vti*us._units.cm/us._units.s), 3)
table[7][4] = round(f.sound_velocity(9.7*us._units.eVt, mass=6.6335209e-26*us._units.kg, charge=2)/(Cs*us._units.cm/us._units.s), 3)
table[8][4] = round(f.Alfven_velocity(130*us._units.G, 1e13*us._units.cm**-3, mass=6.6335209e-26*us._units.kg)/(VA*us._units.cm/us._units.s), 3)
table[9][4] = round(f.Bohm_diffusion(1230*us._units.G, 14.6*us._units.eVt)/(BD*us._units.cm**2/us._units.s), 3)

us.set_unit_system('Gauss-eV')

table[1][5] = round(f.plasma_frequency(1e18*us._units.m**-3, mass=us._constants.me)/wpe, 3)
table[2][5] = round(f.plasma_frequency(1e19*us._units.m**-3, mass=6.6335209e-26*us._units.kg, charge=2)/wpi, 3)
table[3][5] = round(f.gyro_frequency(750*us._units.G, mass=us._constants.me)/wce, 3)
table[4][5] = round(f.gyro_frequency(625*us._units.G, mass=6.6335209e-26*us._units.kg, charge=2)/wci, 3)
table[5][5] = round(f.thermal_velocity(8.5*us._units.eVt, mass=us._constants.me)/(vte*us._units.cm/us._units.s), 3)
table[6][5] = round(f.thermal_velocity(12.3*us._units.eVt, mass=6.6335209e-26*us._units.kg)/(vti*us._units.cm/us._units.s), 3)
table[7][5] = round(f.sound_velocity(9.7*us._units.eVt, mass=6.6335209e-26*us._units.kg, charge=2)/(Cs*us._units.cm/us._units.s), 3)
table[8][5] = round(f.Alfven_velocity(130*us._units.G, 1e13*us._units.cm**-3, mass=6.6335209e-26*us._units.kg)/(VA*us._units.cm/us._units.s), 3)
table[9][5] = round(f.Bohm_diffusion(1230*us._units.G, 14.6*us._units.eVt)/(BD*us._units.cm**2/us._units.s), 3)

for row in table:
    print(row)