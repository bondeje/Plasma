# default unit system is MKS SI

import dataclasses

__all__ = ["set_unit_system"]

_system = 'MKS'
_units, _constants = None, None # changed later
_pi = 3.141592653589793 # pi
_c = 29979245800 # speed of light constant (treat as unitless, but equivalent to speed of light in cm/s); for cgs EM coupling
_e = 1.602176634e-19 # electric charge constant (treat as unitless)
_kB = 1.380649e-23 # thermodynamic temperature to energy (Boltzmann's constant)

UNIT_SYSTEMS = {'MKS':      dict( m=1.0, kg=1.0, s=1.0,     A=1.0, cd=1.0, K=1.0,    mol=1.0, K1=1e-11*_c**2,   K2=1e-7,                Alpha=1.0, Lambda=1.0),
                'ESU':      dict(cm=1.0,  g=1.0, s=1.0, statA=1.0, cd=1.0, K=1.0,    mol=1.0, K1=1.0,           K2=1.0/_c**2,           Alpha=1.0, Lambda=4*_pi),
                'EMU':      dict(cm=1.0,  g=1.0, s=1.0,    Bi=1.0, cd=1.0, K=1.0,    mol=1.0, K1=_c**2,         K2=1.0,                 Alpha=1.0, Lambda=4*_pi),
                'Gauss':    dict(cm=1.0,  g=1.0, s=1.0, statA=1.0, cd=1.0, K=1.0,    mol=1.0, K1=1.0,           K2=1.0/_c**2,           Alpha=_c,  Lambda=4*_pi),
                'Gauss-eV': dict(cm=1.0,  g=1.0, s=1.0, statA=1.0, cd=1.0, eVt=1.0,  mol=1.0, K1=1.0,           K2=1.0/_c**2,           Alpha=_c,  Lambda=4*_pi), # this one does not work as I would expect it; this is going to be difficult. I basically have to independently change Temperature and Energy scale. Need a thermal coupling field in UNITS like for the EM fields
                'HL':       dict(cm=1.0,  g=1.0, s=1.0, statA=1.0, cd=1.0, K=1.0,    mol=1.0, K1=1/(4*_pi),     K2=1.0/(4*_pi*_c**2),   Alpha=_c,  Lambda=1.0)}

UNIT_DEFS = {'Current': 
                 {'A':      1.0,            # Ampere
                  'statA':  10/_c,          # stat Amppere for CGS; this is actually a derived unit in ESU, but use this for now to avoid having a derived unit in the primary unit with fractional unit dependencies...yeah, this needs to get cleared up
                  'abA':    10.0,           # abAmp for CGS, see Biot
                  'Bi':     10.0            # Biot for CGS; this is actually a derived unit
                  },
            'Temperature': 
                {'K':       1.0,            # Kelvin
                 'degC':    1.0,            # Celsius
                 'eVt':     _e/_kB},        # thermal eV
            'Time':
                {'s':       1.0             # seconds
                 },
            'Length':
                {'cm':      1e-2,           # centimeter
                 'm':       1.0,            # meter
                 'km':      1e3,            # kilometer
                 'nm':      1e-9,           # nanometer
                 'um':      1e-6,           # micrometer/micron
                 'pm':      1e-12,          # picometer
                 'mm':      1e-3            # megameter
                 },
            'Mass': 
                {'mg':      1e-6,           # milligram
                 'g':       1e-3,           # gram
                 'kg':      1.0             # kilogram
                 },
            'Luminosity':
                {'cd':      1.0             # Candela
                 },
            'Number':
                {'mol':     1.0             # mole; Avogadro's number
                 },
            'CCoupling':                    # Coulomb/electric force coupling
                {'K1':      1e-11*_c**2},
            'ACoupling':                    # Ampere/magnetic force coupling, NOTE: this is not really an independent "unit" K1/K2 = c**2 for c in whatever unit system is used
                {'K2':      1e-7},
            'FCoupling':                    # Faraday coupling between electric and magnetic field
                {'Alpha':   1.0},
            'MatterCoupling':               # Coupling to macroscopic/continuous media fields
                {'Lambda':  1.0},
            'Derived':                      # SI should be in SI Base Units, cgs in cgs
                {
                   'rad': (1.0, ''),                  # radian
                   'sr':  (1.0, ''),                  # steradian
                   'Hz':  (1.0, 's**-1'),             # Herz
                   'N':   (1.0, 'kg*m*s**-2'),        # Newton
                   'Pa':  (1.0, 'N*m**-2'),           # Pascal
                   'J':   (1.0, 'N*m'),               # Joule
                   'W':   (1.0, 'J*s**-1'),           # Watt
                   'C':   (1.0, 'A*s'),               # Coulomb
                   'V':   (1.0, 'W*A**-1'),           # Volt
                   'F':   (1.0, 'C*V**-1'),           # Farad
                   'Ohm': (1.0, 'V*A**-1'),           # Ohm
                   'S':   (1.0, 'A*V**-1'),           # Siemen
                   'Wb':  (1.0, 'V*s*Alpha'),         # Weber, Alpha factor to account for Gauss/HL EM coupling
                   'T':   (1.0, 'Wb*m**-2'),          # Tesla, Alpha factor accounted for in weber
                   'H':   (1.0, 'V*s*A**-1*Alpha'),   # Henry, Alpha factor to account for Gauss/HL EM coupling
                   'lm':  (1.0, 'cd*sr'),             # lumen (luminous flux)
                   'lx':  (1.0, 'cd*sr*m**-2'),       # lux (illuminance)
                   'Bq':  (1.0, 's**-1'),             # becquerel
                   'Gy':  (1.0, 'm**2*s**-2'),        # gray
                   'Sv':  (1.0, 'm**2*s**-2'),        # Sievert
                   'kat': (1.0, 'mol*s**-1'),         # katal (catalytic activity)
                   'min': (60.0, 's'),                # minute
                   'h':   (3600, 's'),                # hour
                   'd':   (86400, 's'),               # day
                   'au':  (149597870700, 'm'),        # astronomical unit
                   'deg': (_pi/180, 'rad'),           # angular degree
                   'dmin':(_pi/10800, 'rad'),         # angular minute
                   'dsec':(_pi/648000, 'rad'),        # angular second
                   'ha':  (1e4, 'm**2'),              # hectare
                   'L':   (1e-3, 'm**3'),             # liter
                   't':   (1e3, 'kg'),                # (metric) tonne
                   'Da':  (1.66053906660e-27, 'kg'),  # dalton mass unit
                   'eV':  (_e, 'C*V'),                # electron volt, this really should be related 
                                                      # to the constant electrical charge, but that would create circular definisions
                  # CGS, those with * after must be clarified/confirmed with tests
                  'dyn':     (1.0, 'g*cm*s**-2'),        # dyne
                  'atm':     (1013250, 'dyn*cm**-2'),    # atmospheres
                  'Ba':      (1.0, 'dyn*cm**-2'),        # barye
                  'erg':     (1.0, 'dyn*cm'),            # erg
                  'statC':   (1.0, 'statA*s'),           # stat Coulomb
                  'statV':   (1.0, 'erg*statC**-1'),     # stat Volt
                  'statF':   (1.0, 'statV*statC**-1'),   # stat Farad
                  'statOhm': (1.0, 'statV*statA**-1'),   # stat Ohm
                  'statWb':  (1.0, 'statV*s*Alpha'),     # statWeber, Alpha factor to account for Gauss/HL EM coupling
                  'statT':   (1.0, 'statWb*cm**-2'),     # stat Tesla, Alpha factor accounted for in statweber
                 
                  'abC':     (1.0, 'Bi*s'),                     # abCoulomb
                  'abV':     (1.0, 'erg*abC**-1'),              # abVolt
                  'abF':     (1.0, 'abV*abC**-1'),              # abFarad, dubiously used. It is an absurd capacitance & not practical
                  'abOhm':   (1.0, 'abV*Bi**-1'),               # abOhm
                  'Mx':      (1.0, 'abV*s*Alpha'),              # Maxwell, Alpha factor to account for Gauss/HL EM coupling
                  'G':       (1.0, 'Mx*cm**-2'),                # Gauss, Alpha factor accounted for in maxwell
                  'Oe':      (1/(4*_pi), 'Bi*cm**-1*Lambda'),   # Oersted, 4*_pi and Lambda factor makes the conversions consistent when in SI and with the correct scale when in EMU/Gauss, but it is incorrect when converting to oersted from other systems when in EMU/Gauss
                  'abH':     (1.0, 'Mx*Bi**-1')                 # abHenry
                }
                }
    
UNIT_SYMBOLS = {u: ks for ks in UNIT_DEFS.keys() for u in UNIT_DEFS[ks].keys()}

# SI prefixes, in order for the conversion logic to work cleanly, multipliers must be single character
MULTIPLIERS = {'Y': 1e24, # yotta
               'Z': 1e21, # zetta
               'E': 1e18, # exa
               'P': 1e15, # peta
               'T': 1e12, # tera
               'G': 1e9, # giga
               'M': 1e6, # mega
               'k': 1e3, # kilo
               'h': 1e2, # hecto
               # deka will not be used as it is two characters
               'd': 1e-1, # deci
               'c': 1e-2, # centi
               'm': 1e-3, # milli
               'u': 1e-6, # micro
               'n': 1e-9, # nano
               'p': 1e-12, # pico
               'f': 1e-15, # femto
               'a': 1e-18, # atto
               'z': 1e-21, # zepto
               'y': 1e-24} # yocto

CONSTANT_DEFS = {
                  'c': (299792458, 'm*s**-1'),                   # speed of light
                  'h': (6.62607015e-34, 'J*s'),                  # Planck's constant
                  'hbar': (1.054571817e-34, 'J*s'),              # reduced Planck's constant
                  'G': (6.67430e-11, 'm**3*kg**-1*s**-2'),       # Gravitational constant
                  'e0': (1/(4*_pi), 'K1**-1*Lambda'),            # Vacuum electric permittivity
                  'u0': (4*_pi, 'Alpha**2*K2*Lambda**-1'),       # Vacuum magnetic permeability
                  'e': (1.602176634e-19, 'C'),                   # elementary charge
                  'NA': (6.02214076e23, 'mol**-1'),              # Avogadro's constant
                  'kB': (1.380649e-23, 'J*K**-1'),               # Boltzmann's constant
                  'uB': (9.2740100783e-24, 'J*T**-1'),           # Bohr magneton
                  'uN': (5.0507837461e-27, 'J*T**-1'),           # Nuclear magneton
                  'alpha': (7.2973525693e-3, ''),                # fine-structure constant
                  'me': (9.1093837015e-31, 'kg'),                # electron mass
                  'mp': (1.67262192369e-27, 'kg'),               # proton mass
                  'mn': (1.67492749804e-27, 'kg'),               # neutron mass
                  'a0': (5.29177210903e-11, 'm'),                # Bohr radius
                  're': (2.8179403262e-15, 'm'),                 # classical electron radius
                  'ge': (-2.00231930436256, ''),                 # electron g-factor
                  'R': (10973731.568160, 'm**-1'),               # Rydberg constant
                  'sigma': (5.670374419e-8, 'W*m**-2*K**-4')     # Stefan-Boltzmann constant
                 }

unit_factory = dataclasses.make_dataclass('Units', [(s, float) for s in UNIT_SYMBOLS.keys()])
constant_factory = dataclasses.make_dataclass('Constants', [(s, float) for s in CONSTANT_DEFS.keys()])

def update(**kwargs):
    for unit, new_value in kwargs.items():
        unit_class = UNIT_SYMBOLS[unit]
        multiplier = new_value/UNIT_DEFS[unit_class][unit]
        for k in UNIT_DEFS[unit_class].keys():
            UNIT_DEFS[unit_class][k] *= multiplier

# TODO: implement acceptance of SI prefixes, but the use case is not so clear yet
def evaluate_unit_str(unit_val):
    if type(unit_val) == str:
        if unit_val == '':
            return 1.0
        elif unit_val in UNIT_SYMBOLS:
            if type(UNIT_DEFS[UNIT_SYMBOLS[unit_val]][unit_val]) == float: # TODO: need to identify numeric, but not necessarily float
                return UNIT_DEFS[UNIT_SYMBOLS[unit_val]][unit_val]
            else: # derived unit
                return UNIT_DEFS[UNIT_SYMBOLS[unit_val]][unit_val][0] * evaluate_unit_str(UNIT_DEFS[UNIT_SYMBOLS[unit_val]][unit_val][1])
        else: # string is combination of ([SI prefix]unit[**integer/floating power])*
            units = unit_val.split('*')
            converted = []
            i = 0
            while i < len(units):
                if units[i] == '': # next item in [**integer/floating power]
                    i += 1
                    converted[-1] = converted[-1]**float(units[i])
                else: # [SI prefix]unit. TODO: see above specification
                    converted.append(evaluate_unit_str(units[i]))
                i += 1
            prod = 1.0
            for c in converted:
                prod *= c
            return prod
    else:
        return unit_val
    
# TODO allow multiple unit systems to exist simultaneously; 
# being able to load units & constants based on a selected system. 
# Until then, this module acts as the global manager of the units and constants systems
# TODO code smell...should define the systems as constants...dictionary of dictionary
def get_unit_system(system = _system):
    global _system
    if system != _system and system in UNIT_SYSTEMS:
        update(**UNIT_SYSTEMS[system])
        _system = system
    _dict = {}
    for _type in UNIT_DEFS.keys():
        for k, v in UNIT_DEFS[_type].items():
            if type(v) == tuple:
                _dict[k] = v[0]*evaluate_unit_str(v[1])
            else:
                _dict[k] = v
    return unit_factory(**_dict)

# TODO allow an input of a unit system and return constant_factory corresponding to that unit system
# independent of the globals within this module
def get_constants():
    return constant_factory(**{k: v[0]*evaluate_unit_str(v[1]) for k, v in CONSTANT_DEFS.items()})

def set_unit_system(system = _system):
    global _units, _constants
    _units = get_unit_system(system)
    _constants = get_constants()
    return _units, _constants
