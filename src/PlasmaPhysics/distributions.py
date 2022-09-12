# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 21:16:58 2022

@author: jeffrey bonde
"""

from numpy import nan_to_num, Inf, exp, sqrt, pi
from scipy.special import hyperu


# nomenclature strategy is to have '2d', '3d', 'nd' suffixes for multi-dimensional distributions. 
# no suffixed implies '1d'

# function signatures should adhere to statistical definitions, not physical since some of them, like the Kappa distribution, still have controversial physical interpretations

# I really do not think this is the best way to do this...probably should be removed entirely
def Delta(x, loc = 0):
    return nan_to_num((x==loc)*Inf)

def Normal(x, loc = 0, scale = 1):
    if scale == 0:
        return Delta(x, loc)
    return exp(-.5*((x-loc)/scale)**2)/sqrt(2*pi*scale**2)

def Cauchy(x, loc = 0, scale = 1):
    if scale == 0:
        return Delta(x, loc)
    return 1/(1+((x-loc)/scale)**2)/(pi*scale)

# Kappa-Cookbook from Scherer - the Kappa-Cookbook
# TODO: confirm whether scale is equivalent to the thermal velocity consistent with "scale" in Normal(x, loc, scale) in the limit eta --> np.Inf
# TODO: determine what happens when scale-->0 and clear up what to do when eta --> 0, zeta < 0, or xi < 0
# TODO: need to handle where any of eta=0, zeta=2.5, and xi=0 since hyperu has singularities at any of a=0, b=0, x=0 for U(a, b, x)
def KappaCookbook(x, loc = 0, scale = 1, eta = 9/4, zeta = 13/4, xi = 0.0):
    return (1+((x-loc)/(eta**.5*scale))**2)**(-zeta)*exp(-xi*((x-loc)/scale)**2)/(eta*(pi**.5*scale)**3*hyperu(1.5, 2.5-zeta, xi*eta)) # this only works if 2.5-zeta < 1 and xi != 0 and eta != 0
    
# See Scherer - The Kappa-Cookbook
# scale is the Theta parameter. see TODO in KappaCookbook
def RegularizedKappa(x, loc = 0, scale = 1, kappa = 9/4, alpha = 1.0):
    return KappaCookbook(x, loc, scale, kappa, kappa+1, alpha**2)

# standard kappa distribution of Vasyliunas
# scale is the Theta parameter. see TODO in KappaCookbook
def Kappa(x, loc = 0, scale = 1, kappa = 9/4):
    if kappa <= 1.5:
        raise ValueError(f"Invalid input for kappa index {kappa} in standard kappa distribution, kappa > 3/2 is required")
    return KappaCookbook(x, loc, scale, kappa, kappa+1, 0)

