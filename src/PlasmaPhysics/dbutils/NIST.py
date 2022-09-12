# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 21:21:26 2022

@author: jeffrey bonde

this is a very basic HTTP request to the NIST atomic lines and levels databases via their forms
it is not the most complete nor safest, but gets the job done simply and quickly

EXAMPLES:
to view the valid input keywords and their possible values, type
    query_help('Levels') or query_help('Lines')

to get data in dictionary form (all entries are strings because even numerics will have indeterminate non-digit characters added)
    query('lines', Spectrum='C II', Lower='200', Upper='900', Energy_Units='eV')
    -->grabs all data in the C+1 ion spectrum from 200 to 900 nm with energy units given in eV; otherwise use default parameters
    
    query('levels', Spectrum='C I')
    -->grabs all available energy level data for the C+1 ion
    
NOTES:
    default form parameters will expose as much of the data that is possible with as few limitations as possible

    it may not work for every possible configuration of the form (some parameters enable/disable others, which must then be made consistent; I have not yet implemented this)

"""

import requests

NIST_LINES_FORM = 'https://physics.nist.gov/cgi-bin/ASD/lines1.pl'
NIST_LEVELS_FORM = 'https://physics.nist.gov/cgi-bin/ASD/energy1.pl'
IONIZATION_LEVEL_ID = ('Term', 'Limit')
ZERO_CHAR = ord('0')
TEN_CHAR = ord('9') + 1
a_CHAR = ord('a')
z_CHAR = ord('z')
STATE_ID = 'Level (eV)' # this needs to be the key in the table that uniquely or mostly uniquely defines a state. Need a way around in case uniquely identifying states with this key is not possible
ELEMENT_SYMBOLS = ['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl',
                   'Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As',
                   'Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In',
                   'Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb',
                   'Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl',
                   'Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk',
                   'Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs']
Z = [i+1 for i in range(len(ELEMENT_SYMBOLS))]
NIST_ELEMENTS_BIMAP = {k: v for k, v in list(zip(ELEMENT_SYMBOLS, Z)) + list(zip(Z, ELEMENT_SYMBOLS))} # these do not guarantee that the ionization state has a valid spectrum
del Z # this should not be a global

# TODO move to a utilities module
# returns None if input not valid roman numeral
def roman_to_int(s):
    rtoi = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
    
    i = 0
    lastval = 0
    nextval = 0
    for ch in s[::-1]:
        if not ch in rtoi:
            return None # shortcircuit as invalid roman numeral
        nextval = rtoi[ch]
        i += nextval if nextval>=lastval else -1*nextval
        lastval = nextval
    
    return i

# TODO move to a utilities module
# returns None if num <= 0 since roman numeral does not exist
def int_to_roman(num: int) -> str:
    if num <= 0:
        return None
    mIntToRom = {1000:"M", 900:"CM", 500:"D", 400:"CD", 100:"C", 90:"XC", 50:"L", 40:"XL", 10:"X", 9:"IX", 5:"V", 4:"IV", 1:"I"}
    
    roman = ''
    for k,v in mIntToRom.items():
        if num == 0:
            break
        quot, num = divmod(num, k)
        roman += quot*v
        
    return roman

# TODO create spectroscopy package adn move this there
# TODO convert ionization notation to spectroscopic notation (for elements), i.e. C3+ to C IV or C+ to C II (space is required)
# Note: there is no negative charge for spectroscopic notation, so it does not work here. Currently returns None
# WARNING: int_to_roman will move from NIST in the future
def ionization_to_spectroscopic(label):
    N = len(label)
    charge = 0
    if label[-1] == '+':
        charge = 1
        right = N-1
    elif label[-1] == '-':
        charge = -1
        right = N-1
    else:
        right = N
    left = 0
    while left < right and not (ZERO_CHAR <= ord(label[left]) < TEN_CHAR):
        left += 1
    el = label[:left].strip()
    if left < right:
        charge *= int(label[left:right])
    
    if charge >= 0:
        return el + ' ' + int_to_roman(charge + 1)
    else:
        return None

# TODO create spectroscopy package adn move this there
# TODO convert spectroscopic notation to ionization notation (for elements), i.e. C IV to C2+
# Note: there is no negative charge for spectroscopic notation, so it does not work here
# WARNING: roman_to_int will move from NIST in the future
def spectroscopic_to_ionization(label):
    label = label.strip().split(' ')
    el, chargep1 = label[0], roman_to_int(label[1])
    return el + str(chargep1-1) + '+'

# Returns name of ion, charge of ion, ionization energy, states dictionary with STATE_ID as key
# Returns None if ion is invalid
def get_ion_description(ion):
    if not is_valid_NIST_spectra(ion):
        old = ion
        ion = ionization_to_spectroscopic(ion)
        if not is_valid_NIST_spectra(ion):
            raise Warning(f"could not resolve ion={old} in NIST.get_ion_description. None returned.")
            return tuple([None]*4)
    name, charge = ion.split(' ')
    charge = roman_to_int(charge)-1
    
    state_spec = {}
    table = query('levels', Spectrum=ion, attempt_numeric=True, Units='eV', Order='Energy')
    if not table:
        return name, charge, None, state_spec
    headers = table.keys()
    pars_to_headers = {split_units(k)[0].lower(): k for k in headers}
    Nlevels = len(table[STATE_ID])
    
    ionization_energy = max(table[STATE_ID])
    for i in range(Nlevels):
        if IONIZATION_LEVEL_ID[0] in headers and table[IONIZATION_LEVEL_ID[0]] == IONIZATION_LEVEL_ID[1]:
            ionization_energy = table[STATE_ID][i]
        else:
            state = {}
            _id = table[STATE_ID][i]
            for par, header in pars_to_headers.items():
                state[par] = table[header][i]
            if _id in state_spec:
                state_spec[_id].append(state)
            else:
                state_spec[_id] = [state]
    return name, charge, ionization_energy, state_spec

def is_valid_NIST_spectra(label, try_harder=False):
    label = label.strip().split(' ')
    if len(label) != 2:
        return False
    el, chargep1 = label[0], roman_to_int(label[1])
    # chargep1 (charge + 1) must be a positive integer, el must be in the BiMap and point to the proton number, Z, chargep1 can at most be Z+1
    if chargep1 is None or not el in NIST_ELEMENTS_BIMAP or not type(NIST_ELEMENTS_BIMAP[el]) == int or chargep1>NIST_ELEMENTS_BIMAP[el]+1:
        return False
        
    return True

# these namespace variables should be hard-coded in a json and loaded at import
VALID_LINES_KWARGS = {'Spectrum': 'spectra',
                'Lower': 'low_w',
                'Upper': 'upp_w',
                'Limits': {'name': 'limits_type',
                           'Wavelengths': '0',
                           'Wavenumbers': '1'},
                'Wavelength_Units': {'name': 'unit',
                                     'A': '0',
                                     'nm': '1',
                                     'um': '2'},
                'Line_Reqs': {'name': 'line_out',
                          'All': '0',
                          'Transitions': '1',
                          'Energy_Levels': '2',
                          'Observed_Wavelengths': '3',
                          'Diagnostics': '4'},
                'Energy_Units': {'name': 'en_unit',
                                 'cm-1': '0',
                                 'eV': '1',
                                 'R': '2'},
                'Observed': {'name': 'show_obs_wl',
                             True: '1',
                             False: None},
                'Ritz': {'name': 'show_calc_wl',
                         True: '1',
                         False: None},
                'Difference': {'name': 'show_odiff_obs_calc',
                               True: '1',
                               False: None},
                'Wavenumber': {'name': 'show_wn',
                               True: '1',
                               False: None},
                'Uncertainty': {'name': 'unc_out',
                                  True: '1',
                                  False: None},
                'Max_Lower_Level_Enerry': 'max_low_enrg',
                'Max_Upper_Level_Energy': 'max_low_enrg',
                'Wavelengths_In': {'name': 'show_av',
                                'VacuumAirWavenumber': '0',
                                'VacuumWavenumber': '1',
                                'VacuumAirVacuum': '2',
                                'Vacuum': '3',
                                'VacuumAir': '4',
                                'Wavenumber': '5'},
                'Energy': {'name': 'enrg_out',
                           True: 'on',
                           False: None},
                'Configuration': {'name': 'conf_out',
                                  True: 'on',
                                  False: None},
                'Term': {'name': 'term_out',
                         True: 'on',
                         False: None},
                'J': {'name': 'j_out',
                      True: 'on',
                      False: None},
                'g': {'name': 'g_out',
                      True: 'on',
                      False: None}}

DEFAULT_LINES_QUERY = {'spectra': 'H I',
                 'limits_type': '0',
                 'low_w': '200',
                 'upp_w': '1000',
                 'unit': '1',
                 'submit': 'Retrieve Data',
                 'de': '0',
                 'format': '2', # DO NOT CHANGE without adding functionality in parser
                 'line_out': '0',
                 'en_unit': '0',
                 'output': '0', # DO NOT CHANGE; '1' splits into separate pages
                 'bibrefs': None, # unused
                 'page_size': '15',
                 'show_obs_wl': '1',
                 'show_calc_wl': '1',
                 'show_diff_obs_calc': '1',
                 'show_wn': '1',
                 'unc_out': '1',
                 'order_out': '0',
                 'max_low_enrg': '',
                 'show_av': '2',
                 'max_upp_enrg': '',
                 'tsb_value': '0',          # TODO for VALID_KWARGS
                 'min_str': '',             # TODO for VALID_KWARGS
                 'A_out': '0',              # TODO for VALID_KWARGS
                 'f_out': 'on',             # TODO for VALID_KWARGS
                 'S_out': 'on',             # TODO for VALID_KWARGS
                 'loggf_out': 'on',         # TODO for VALID_KWARGS
                 'intens_out': 'on',        # TODO for VALID_KWARGS
                 'max_str': '',             # TODO for VALID_KWARGS
                 'allowed_out': '1',        # TODO for VALID_KWARGS
                 'forbid_out': '1',         # TODO for VALID_KWARGS
                 'min_accur': '',           # TODO for VALID_KWARGS
                 'min_intens': '',          # TODO for VALID_KWARGS
                 'conf_out': 'on',          
                 'term_out': 'on',
                 'enrg_out': 'on',
                 'J_out': 'on',
                 'g_out': 'on'}

VALID_LEVELS_KWARGS = {'Spectrum': 'spectrum',
                'Units': {'name': 'units',
                                 'cm-1': '0',
                                 'eV': '1',
                                 'R': '2'},
                'Order': {'name': 'multiplet_ordered',
                                'Term': '0',
                                'TermEnergy': '1',
                                'Energy': '2'},
                'Configuration': {'name': 'conf_out',
                                  True: 'on',
                                  False: None},
                'Term': {'name': 'term_out',
                         True: 'on',
                         False: None},
                'Level': {'name': 'level_out',
                           True: 'on',
                           False: None},
                'Uncertainty': {'name': 'unc_out',
                                  True: '1',
                                  False: None},
                'J': {'name': 'j_out',
                      True: 'on',
                      False: None},
                'g': {'name': 'g_out',
                      True: 'on',
                      False: None},
                'Lande-g': {'name': 'lande_out',
                      True: 'on',
                      False: None},
                'LeadingPercentages': {'name': 'perc_out',
                      True: 'on',
                      False: None}}


DEFAULT_LEVELS_QUERY = {
    'spectrum': 'H I',
    'units': '1',
    'parity_limit': 'both',
    'conf_limit': 'All',
    'term_limit': 'All',
    'format': '2', # DO NOT CHANGE without adding functionality in parser
    'output': '0', # DO NOT CHANGE; '1' splits into separate pages
    'page_size': '15',
    'multiplet_ordered': '2',
    'conf_out': 'on',
    'term_out': 'on',
    'level_out': 'on',
    'unc_out': 'on',
    'j_out': 'on',
    'g_out': 'on',
    'lande_out': 'on',
    'perc_out': 'on',
    'biblio': None,
    'splitting': '1',
    'submit': 'Retrieve Data'}

HEADER_MAP = {'element': 'Element',
              'sp_num': 'Charge',
              'obs_wl_air': 'Observed Wavelength',
              'unc_obs_wl': 'Obs. Unc.',
              'ritz_wl_air': 'Ritz Wavelength',
              'unc_ritz_wl': 'Ritz Unc.',
              'obs-ritz': 'Obs. - Ritz',
              'wn': 'Wavenumber',
              'intens': 'Rel. Int.',
              'Aki': 'Aki',
              'fik': 'fik',
              'S': 'S',
              'log_gf': 'log(gi fik)',
              'Acc': 'Acc.',
              'Ei': 'Ei',
              'Ek': 'Ek',
              'conf_i': 'Lower Conf.',
              'term_i': 'Lower Term',
              'J_i': 'Lower J',
              'conf_k': 'Upper Conf.',
              'term_k': 'Upper Term',
              'J_k': 'Upper J',
              'g_i': 'gi',
              'g_k': 'gk',
              'Type': 'Type',
              'tp_ref': 'TP Ref.',
              'line_ref': 'Line Ref.'}

def convert_headers(headers):
    i = 0
    while i < len(headers):
        loc = headers[i].find('(')
        if loc >= 0:
            hdr = headers[i][:loc]
            rem = ' ' + headers[i][loc:]
        else:
            hdr = headers[i]
            rem = ''
        
        if hdr in HEADER_MAP:
            headers[i] = HEADER_MAP[hdr] + rem
        i += 1
    return headers

# def strip_units(header):
#     return header.split('(')[0].strip()

def split_units(header):
    header = header.strip().split('(')
    if len(header) == 2:
        return header[0].strip(), header[1].strip().split(')')[0].strip()
    else:
        return header[0], None

# a number defined here is ^[+-](?<![a-z])[0-9]*[.][0-9](?![a-z])
def extract_numeric(val):
    ind = val.find('/')
    N = len(val)
    if 0 < ind < N-1:
        num = extract_numeric(val[:ind])
        den = extract_numeric(val[ind+1:])
        if type(num) == float and type(den) == float:
            return num/den
    
    left, right = 0, N
    while left < right:
        if val[left] == '+' or val[left] == '-' or val[left] == '.' or ZERO_CHAR <= ord(val[left]) < TEN_CHAR:
            break
        elif a_CHAR <= ord(val[left].lower()) <= z_CHAR:
            return val
        left += 1
        
    while right-1 > left:
        ind = right-1
        if val[ind] == '.' or ZERO_CHAR <= ord(val[ind]) < TEN_CHAR:
            break
        elif a_CHAR <= ord(val[ind].lower()) <= z_CHAR:
            return val
        right -= 1
        
    if right <= left:
        return val
    else:
        try:
            return float(val[left:right])
        except ValueError:
            return val

def to_table(response, attempt_numeric=False):
    lines = str(response.text).replace('"','').replace('=','').split('\n')
    headers = convert_headers(lines[0].split(',')[:-1])
    result = {header:[] for header in headers}

    for line in lines[1:]:
        for i, el in enumerate(line.split(',')[:len(headers)]):
            val = el.strip()
            if attempt_numeric:
                extracted = extract_numeric(val)
                if type(extracted) != str:
                    val = extracted
            result[headers[i]].append(val)
    return result

def add_params(valid_input, user_input = None, default = None):
    if user_input is None:
        user_input = {}
    if default is None:
        default = {}
                
    Q = list(user_input.keys())
    while Q:
        k = Q.pop()
        opt = k.strip().replace(" ", "_")
        if opt in valid_input:
            if type(valid_input[opt])==dict:
                val = user_input.pop(k)
                try:
                    user_input[valid_input[opt]['name']] = valid_input[opt][val]
                except KeyError:
                    print(f"Invalid option selected for {k} = {val}, only {','.join([str(j) for j in VALID_LINES_KWARGS[opt].keys() if not j=='name'])} accepted")
            else:
                user_input[valid_input[opt]] = str(user_input.pop(k))

    return {**default, **user_input}

def query(query_type, attempt_numeric=False, **kwargs):
    if query_type.lower() == 'lines':
        valid = VALID_LINES_KWARGS
        defaults = DEFAULT_LINES_QUERY
        form = NIST_LINES_FORM
    elif query_type.lower() == 'levels':
        valid = VALID_LEVELS_KWARGS
        defaults = DEFAULT_LEVELS_QUERY
        form = NIST_LEVELS_FORM
    else:
        print('Selected query type not understood. Please use "levels" or "lines" (case insensitive)')
        return {}
    
    return to_table(requests.get(form, params=add_params(valid, kwargs, defaults)), attempt_numeric=attempt_numeric)

def query_help(query_type):
    if query_type.lower() == 'lines':
        valid = VALID_LINES_KWARGS
    elif query_type.lower() == 'levels':
        valid = VALID_LEVELS_KWARGS
    else:
        print('Selected query type not understood. Please use "levels" or "lines" (case insensitive)')
        return
    
    for k, v in valid.items():
        if type(v)==dict:
            print(f"{k} - options: {','.join([str(j) for j in v.keys() if not j=='name'])}")
        else:
            print(f"{k} - string")

if __name__=="__main__":
    lines = query('lines', Spectrum='C II', Lower='200', Upper='900', Energy_Units='eV')
    levels = query('levels', Spectrum='C II')