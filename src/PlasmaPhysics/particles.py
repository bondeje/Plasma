# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 08:10:56 2022

@author: jeffr
"""

# module for defining particles and their interactions

import abc
import numpy as np
from dataclasses import dataclass
from .dbutils import NIST # NOTE: all energies from NIST are in eV

STATE_CLASSES = {'electronic', 'nuclear'}

# UNUSED
# @dataclass
# class AtomState:
#     configuration: str = ''
#     term: str = ''
#     J: float = 0.0
#     g: float = 0.0
#     energy: float = 0.0
#     splitting: float = 0.0

# abstract base class
class Movable(metaclass=abc.ABCMeta):
    # all Movables must have a position, momentum, and ang_momentum
    def __init__(self, position: np.array=None, momentum: np.array=None, ang_momentum: np.array=None, *arg, **kwargs):
        if position is None:
            self.position = np.array([0,0,0])
        else:
            self.position = position
        if momentum is None:
            self.momentum = np.array([0,0,0])
        else:
            self.momentum = momentum
        if ang_momentum is None:
            self.ang_momentum = np.array([0,0,0])
        else:
            self.ang_momentum = ang_momentum
    
    # This is effectively the setter for both position and momentum but did not want to bloat with setters/deleters
    # for integrating a pusher/integrator. Just have a separate method that uses the position and momentum and calls
    # move internally to update. This really is just a basic typing interface
    @abc.abstractmethod
    def move(self, dposition=None, dmomentum=None, dang_momentum=None):
        pass    

# (elementary) particles are basically just data structures capturing the state of an entity
# ex.s: electrons are particles, but atoms are not
# further ex.s: photons are particles, protons can be but need not be (they can be considered collections of quarks, which are particles)
# particles may or may not have all of the state items below
# as a subclass of Movable, this must have definite position and momentum values that can be updated; for quantum effects, use this to keep track of state expected positions and momenta
@dataclass
class Particle(Movable):
    position: np.ndarray = None # TODO: this really just be an iterable
    momentum: np.ndarray = None # TODO: this should just be an iterable
    ang_momentum: np.ndarray = None # TODO: this should just be an iterable
    charge: float = 0 
    mass: float = 0
    spin: float = None
    color: str = None
    name: str = None # optional; probably should get rid of this
    
    def move(self, dposition=None, dmomentum=None, dang_momentum=None):
        if not dposition is None:
            for i in range(len(dposition)):
                self.position[i] += dposition[i]
        if not dmomentum is None:
            for i in range(len(dmomentum)):
                self.momentum[i] += dmomentum[i]
        if not dang_momentum is None:
            for i in range(len(dang_momentum)):
                self.ang_momentum[i] += dang_momentum[i]


# an atom is not a particle
# observed that it clearly can contain particles and satisfies a similar interface (Movable), but it clearly is a composition
# in order to fit within the most common paradigms of behaving like a traditional "particle", it must satisfy an interface
# if 'states' is a string corresponding to a pre-defined type of atom in spectroscopic, e.g. C IV, or ionization notation, e.g. C3+, then name, charge, ionization_energy
# components is an unused constructor argument to be used for when we want to populate the Atom with particles, e.g. to identify isotopes and account for nuclear phenomena
# but this will require identifying more than just spectroscopic or ionization notation
class Atom(Movable):
    
    ENERGY_TOLERANCE = 1e-7
    
    position: np.ndarray
    momentum: np.ndarray
    ang_momentum: np.ndarray
    
    def __init__(self, position: np.array=None, momentum: np.array=None, ang_momentum: np.array=None, mass: float=0.0, charge: int=0, states = None, components=None):
        super().__init__(position, momentum, ang_momentum)
        self.mass = mass
        self.states = {}
        self.state = {}
        if type(states) == str: # need to also validate whether state_pec is in 
            self.name, self.charge, self.ionization_energy, electronic_states = NIST.get_ion_description(states)
            if electronic_states:
                self.states['electronic'] = electronic_states
                self.state['electronic'] = list(self.states['electronic'].keys())[0] # should already be sorted with ground state first
        else:
            validity = Atom.is_valid_state_description(states)
            if validity:
                if validity == 2:
                    self.states = states
                elif validity == 1:
                    self.states = {_class: {k: v for k, v in sorted(states[_class].items(), key=lambda x: x[0])} for _class in states.keys()}
                for k in self.states.keys():
                    self.state[k] = list(self.states[k].keys())[0] # set to ground state for each class
            # else: do not set self.states/self.state
            self.charge = charge
            self.name = 'custom atom'
        self.components = None
    
    def move(self, dposition=None, dmomentum=None, dang_momentum=None):
        if not dposition is None:
            for i in range(len(dposition)):
                self.position[i] += dposition[i]
        if not dmomentum is None:
            for i in range(len(dmomentum)):
                self.momentum[i] += dmomentum[i]
        if not dang_momentum is None:
            for i in range(len(dang_momentum)):
                self.ang_momentum[i] += dang_momentum[i]
    
    @classmethod
    # return 0 if invalid, 1 if valid, 2 if valid and energy/key are sorted floating values
    def is_valid_state_description(cls, states):
        if states is None:
            return 0
        result = 2
        for _class in states.keys():
            if not _class in STATE_CLASSES:
                return 0
            keys = list(states[_class].keys())
            if not keys is None and len(keys) > 0:
                if result > 1:
                    N = len(keys)
                    i = 1
                    while i < N and keys[i] >= keys[i-1]:
                        i += 1
                    result = 2 if i == N else 1
            else:
                return 0
        return result
    
    # TODO
    # negative energy is de-excitation, which should add a photon (or others)
    # returns references to objects created/modified by the process
    def excite(self, energy, interaction_type='electronic'):
        pass
        return [self]