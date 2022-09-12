# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 17:11:52 2022

@author: jeffrey bonde
"""

import sys
from . import unitsystems # must be separate and first
from .unitsystems import set_unit_system as sus

__all__ = ["dbutils",
           "dispersion",
           "distributions",
           "formulary",
           "particles",
           "unitsystems",
           "units",
           "constants"]

_system, units, constants = unitsystems._system, None, None

# wrapper for PlasmaPhysics.unitsystems.set_unit_system to allow package globals to be updated/synced with unitsystems' module globals
def set_unit_system(system = _system):
    global units, constants
    #return None, None
    units, constants = sus(system)
    #return unitsystems.set_unit_systems(system)

set_unit_system() # initialize global unit system and constants

from . import dispersion, distributions, formulary

from ._version import get_versions


vinfo = get_versions()
__version__ = vinfo["version"]
require_python = tuple(int(d) for d in vinfo["python"].split('.'))
python_version = tuple(sys.version_info)[:3]

if require_python > python_version:
    raise ImportError(f"module Plasma: requires minimum python version of {vinfo['python']}, found {'.'.join([str(d) for d in python_version])}", name="Plasma")

del get_versions, vinfo, python_version, require_python

