# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 22:20:22 2022

@author: jeffrey bonde
"""

import numpy as np
from scipy.special import wofz
from functools import partial

i = complex(0, 1)

def get_dtype(z):
    try:
        type(z[0])
        return get_dtype(z[0])
    except IndexError:
        return type(z)

# based on Weideman's paper, but not using his code which calculates a number of Fourier coefficients that is neither a minimal number nor an efficient number for fft
def get_fourier_poly_expansion(func, N, L):
    M = int(2**(0+np.ceil(np.log2(2*(N+1))))) # more efficient than Weideman's. Weideman just takes 4*N, but only 2*(N+1) are needed and 2*(N+1) <= 2^k for some k makes the fft very efficient. This calculates that appropriate k
    j = np.linspace(-M/2, M/2-1, M)
    theta = j*np.pi*2/M
    #L = Lfunc(N)
    #L = np.sqrt(N/np.sqrt(2))
    x = L*np.tan(theta/2)
    f = func(x)*(L**2 + x**2) # might underflow for x[0]
    f[0] = 0 # explicit!
    return np.sqrt(np.pi)*np.fft.fft(np.roll(f,M//2))/M[:N+1][::-1] # I suppose the meat of the algorithm and the major difference between my [jeffrey bonde] implementation and Weideman's; I calculate and roll the minimum amount 

# based on Weideman's paper but this is just Horner's rule on the expansion from get_fourier_poly_expansion + analytic continuation to lower half-plane
# TODO: the handling of singleton vs arrays and splitting between upper and lower half-plane needs to be cleaned up. probably would be useful to break out a utility function -- maybe specific to this sub-package -- that separates the upper- and lower- half-planes
def eval_complex_hilbert_transform(z, a, L, func):
    if func is None:
        raise TypeError()
    singleton = False
    
    #N = len(a)-1
    #L = Lfunc(N)
    if not type(z) is np.ndarray:
        singleton = True
        indUpper = np.array([False]) if np.imag(z) < 0 else np.array([True])
        indLower = np.invert(indUpper)
        z = np.array([z])
    else:
        singleton = False
        indUpper = np.imag(z) >= 0 # note from Weideman's paper that == 0 is handled by the expansion without any changes
        indLower = np.invert(indUpper)
    out = np.zeros(z.shape,dtype=get_dtype(z))
    if z[indUpper].size < z.size:    
        out[indUpper] = 2*np.polyval(a[:-1], (L+i*z[indUpper])/(L-i*z[indUpper]))/(L-i*z[indUpper])**2 + a[-1]/L/(L-i*z[indUpper])
        if not callable(func):
            raise TypeError("func argument in 'eval_complex_hilbert_transform is not callable - cannot evaluate in lower half-plane")
        out[indLower] = 2*np.sqrt(np.pi)*func(z[indLower])-eval_complex_hilbert_transform(-z[indLower], a, L, func)
    else:
        out[indUpper] = 2*np.polyval(a[:-1], (L+i*z[indUpper])/(L-i*z[indUpper]))/(L-i*z[indUpper])**2 + a[-1]/L/(L-i*z[indUpper])
    if singleton:
        return out[0]
    else:
        return out
    
# factory function that returns a generalized plasma dispersion function based on the complex Hilbert transform of the fourier sampled distribution function; see Weideman's Computation of the Complex Error Function where we generalize to non-Maxwellian integrands. Note, this is also what Xie's paper does, but that paper is complete garbage and hard to follow. It was easier to just rederive the results of the paper from Weideman.
def GPDF_factory(func, N=16, L=np.sqrt(16/np.sqrt(2))):
    return partial(eval_complex_hilbert_transform, a=get_fourier_poly_expansion(func, N, L), L=L, func=func)

def PDF(z):
    return i*np.sqrt(np.pi)*wofz(z)