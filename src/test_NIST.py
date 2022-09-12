# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 13:35:44 2022

@author: jeffr
"""

from PlasmaPhysics.dbutils import NIST

levels = NIST.query('levels', Spectrum='Ar II', attempt_numeric=True)
print(levels.keys())
for row in zip(*[v for k, v in levels.items() if k in {'Level (eV)', 'Configuration', 'Term', 'J', 'g', 'Splitting'}]):
    print(row)
    
levels2 = NIST.query('levels', Spectrum='Cn I', attempt_numeric=True) # no copernicium spectrum