import numpy as np
from abc import ABCMeta, abstractmethod
from .. import utils
import matplotlib.pyplot as plot
from functools import partial

import warnings
warnings.filterwarnings("error") # for ragged list creation of np.array. Need to have these as exceptions.

DEFAULT_SPACE_DIM = 3
DEFAULT_LOCATION = np.array([0,0,0],dtype=float)
DEFAULT_ORIENTATION = np.array([0,0,1],dtype=float)
# TODO verify a reasonable value for below
DETERMINANT_PRECISION = 1e-7
# TODO verify a reasonable value for below
PRECISION_PER_ELEMENT = 1e-7
POINTS_PER_LENGTH = 10/(2*np.pi)
DEF_OPTIMIZER_PRECISION = 1e-4

def orientation_to_rotation(orientation):
    rot_axis = np.cross(DEFAULT_ORIENTATION, orientation)
    rot_mag = np.linalg.norm(rot_axis)
    angle = np.arcsin( rot_mag / (np.linalg.norm(DEFAULT_ORIENTATION) * np.linalg.norm(orientation)))
    rot_axis *= (angle / rot_mag)
    return rot_axis

def rotation_matrix(axis):
    angle = np.linalg.norm(axis)
    
    if angle == 0:
        return np.eye(DEFAULT_SPACE_DIM)
    
    # TODO: this is essentially hard-coded 3D
    l, m, n, c, s = axis[0]/angle, axis[1]/angle, axis[2]/angle, np.cos(angle), np.sin(angle)
    
    return np.array([[l**2*(1-c) + c, m*l*(1-c) - n*s, n*l*(1-c) + m*s],
                     [l*m*(1-c) + n*s, m**2*(1-c) + c, n*m*(1-c) - l*s],
                     [l*n*(1-c) - m*s, m*n*(1-c) + l*s, n**2*(1-c) + c]], dtype=float)

def reflection_matrix(plane):
    mag = np.linalg.norm(plane[:DEFAULT_SPACE_DIM])
    
    a, b, c, d = plane[0]/mag, plane[1]/mag, plane[2]/mag, plane[3]/mag
    
    # TODO: this is essentially hard-coded 3D
    return np.array([[1-2*a**2, -2*a*b, -2*a*c],
                     [-2*a*b, 1-2*b**2, -2*b*c],
                     [-2*a*c, -2*b*c, 1-2*c**2]], dtype=float), -2*d*np.array([a, b, c], dtype=float)

# once rotation_matrix is tested, delete this
# def _mrot_x(alpha):
#     c = np.cos(alpha)
#     s = np.sin(alpha)
#     return np.array([[1, 0,  0], 
#                      [0, c, -s], 
#                      [0, s,  c]], dtype=float)
# once rotation_matrix is tested, delete this
# def _mrot_y(beta):
#     c = np.cos(beta)
#     s = np.sin(beta)
#     return np.array([[ c, 0, s], 
#                      [ 0, 1, 0], 
#                      [-s, 0, c]], dtype=float)
# once rotation_matrix is tested, delete this
# def _mrot_z(gamma):
#     c = np.cos(gamma)
#     s = np.sin(gamma)
#     return np.array([[c, -s, 0], 
#                      [s,  c, 0], 
#                      [0,  0, 1]], dtype=float)

# There is no class point...just use a coordinate as a np.array of length ndim; data type converted to float
# this copies data, need to have a keyword 'in_place' if we need to do this in place, which will only work for certain input types
# a 3D array will be converted to a 2D array of points, i.e. coord.shape=(n,m,p)-->(n,m,3) where the last dim is the set of points
def format_as_points(coord, ndim=DEFAULT_SPACE_DIM):
    if ndim != DEFAULT_SPACE_DIM:
        raise NotImplementedError(f"non {DEFAULT_SPACE_DIM}D geometries not yet implemented")
    out = None
    if is_point(coord, ndim):
        out = coord[:]
    else:
        if type(coord)==np.ndarray:
            if len(coord.shape) > 1:
                out = np.array([format_as_points(c) for c in coord], dtype=float)
            elif coord.size > ndim:
                out = coord[:ndim]*1.0
            elif coord.size < ndim:
                out = np.zeros(ndim,dtype=float)
                out[:coord.size] = coord[:]
            else:
                out = coord[:]*1.0
        elif utils.is_iterable(coord):
            out = format_as_points(np.array(coord), ndim)
        else:
            raise ValueError(f"invalid input to 'format_as_point'. {coord} must be an iterable")
    return out

def is_point(coord, ndim=DEFAULT_SPACE_DIM):
    if ndim != DEFAULT_SPACE_DIM:
        raise NotImplementedError(f"non {DEFAULT_SPACE_DIM}D geometries not yet implemented")
    return type(coord)==np.ndarray and coord.shape==(DEFAULT_SPACE_DIM,) and isinstance(coord[0], float)

# base geometry class where general methods are place
# note that the affine transformations are not thread safe
class BaseGeometry(metaclass=ABCMeta):
    @abstractmethod
    def translate(self, vector):
        pass
    
    @abstractmethod
    def rotate(self, axis, location=None):
        pass
    
    @abstractmethod
    def reflect(self, plane):
        pass
    
    @abstractmethod 
    def scale(self, vector, location=None):
        pass
    
    # TODO signature not yet defined
    @abstractmethod 
    def shear(self):
        pass
    
    # returns coords as tuple x, y, z
    @abstractmethod
    def draw(self, ax, *args, **kwargs):
        pass
   
# base geometry that is an non-descript collection of points, can be instantiated. If you MUST have a point, use this with only one point
class PointCollection(BaseGeometry):
    def __init__(self, coords): # if ref_point==None, use coords[0] as the center
        self.points = format_as_points(coords)
        if len(self.points.shape) == 1:
            self.points = np.array([self.points])
        elif len(self.points.shape) == 0:
            raise ValueError("Cannot instantiate PointCollection with an empty set of coords")
        self.npoints = self.points.shape[0]
            
        # might want to have an initialization option for how deep the cache is...like a LRU cache. This cache could become enormous
        # for scale transformations, need to reset
        self._dist_cache = {}
    
    # TODO needs to be tested...pretty sure this is right, but need move_ref to be accurate
    # axis may be a single vector or a list of vectors
    def translate(self, vector):
        for i in range(self.npoints):
            self.points[i,:] += vector
            
    # axis may be a single vector or a list of vectors to be compiled as a composite rotation
    # TODO allow list of vector
    def rotate(self, axis, location=None):
        if not axis is None and not all(axis == [0,0,0]):
            if utils.is_iterable(axis[0]):
                R = np.eye(DEFAULT_SPACE_DIM)
                for ax in axis:
                    R = np.matmul(rotation_matrix(format_as_points(ax)), R)
            else:
                R = rotation_matrix(format_as_points(axis))
            if location is None:
                for i in range(self.npoints):
                    self.points[i,:] = np.matmul(R, self.points[i,:])
            else:
                location = format_as_points(location)
                for i in range(self.npoints):
                    self.points[i,:] = np.matmul(R, self.points[i,:]-location) + location
    
    ## overly complicated; once above is tested, delete this
    # # TODO needs to be tested
    # #@extract_to_kwargs(['self', 'alpha', 'beta', 'gamma'])
    # def rotate(self, **kwargs):
    #     if 'R' in kwargs:
    #         if type(kwargs['R']) != np.ndarray:
    #             R = np.array(kwargs['R'])
    #         else:
    #             R = kwargs['R']
    #         if not is_rotation(R):
    #             raise ValueError("matrix input {R} to rotate is not a valid rotation matrix")
    #     else:
    #         R = np.eye(DEFAULT_SPACE_DIM)
    #         for k in kwargs.keys():
    #             kl = k.lower()
    #             if kl == 'alpha':
    #                 M = _mrot_x(kwargs[k])
    #             elif kl == 'beta':
    #                 M = _mrot_y(kwargs[k])
    #             elif kl == 'gamma':
    #                 M = _mrot_z(kwargs[k])
                
    #             R = np.matmul(M, R)
        
    #     for i in range(self.npoints):
    #         self.points[i,:] = np.matmul(R, self.points[i,:] - self._location) + self._location
        
    # plane may be a single vector or a list of vectors
    # TODO: implement for list of planes
    def reflect(self, plane):
        if not plane is None and not all(plane[:DEFAULT_SPACE_DIM] == np.zeros(DEFAULT_SPACE_DIM)):
            if utils.is_iterable(plane[0]):
                raise NotImplementedError("multiple reflection planes not yet implemented")
            else:
                A, b = reflection_matrix(plane)
                for i in range(self.npoints):
                    self.points[i,:] = np.matmul(A, self.points[i,:]) + b
    
    # axis may be a single vector or a list of vectors
    def scale(self, vector, location=None):
        # TODO: implement for list of axes
        if not vector is None and not all(vector == np.zeros(DEFAULT_SPACE_DIM)):
            if utils.is_iterable(vector[0]):
                raise NotImplementedError("multiple scale vectors not yet implemented")
            else:
                S = np.diag(vector)
            if location is None:
                for i in range(self.npoints):
                    self.points[i,:] = np.matmul(S, self.points[i,:])
            else:
                location = format_as_points(location)
                for i in range(self.npoints):
                    self.points[i,:] = np.matmul(S, self.points[i,:]-location) + location
        self._dist_cache.clear()
        
    # TODO: define signature and implementation
    def shear(self):
        # NOTE: this does not preserve relative distances so self._dist_cache needs to be cleared
        raise NotImplementedError("shearing a PointCollection not yet implemented")
        self._dist_cache.clear()
        
    def draw(self, ax, *args, **kwargs):
        ax.scatter3D(self.points[:,0], self.points[:,1], self.points[:,2], *args, **kwargs)
        
    def point_distance(self, p1, p2):
        if p2 < p1:
            return self.point_distance(p2, p1)
        elif p1 < 0:
            return self.point_distance(self.npoints + p1, p2)
        elif p2 >= self.npoints:
            return self.point_distance(p1, p2-self.npoints)
        val = np.sum((self.points[p1] - self.points[p2])**2)**.5
        # for caching
        pair = (p1, p2)
        if not pair in self._dist_cache:
            self._dist_cache[pair] = val
        return val
            
    def __getitem__(self, ind, coord=None):
        if type(ind) == tuple:
            ind, coord = ind
        if ind >= self.npoints:
            return self.__getitem__(ind-self.npoints, coord)
        elif  ind < 0:
            return self.__getitem__(ind+self.npoints, coord)
        if coord is None:
            return self.points[ind,:]
        else:
            return self.points[ind, coord]
    
class Curve(BaseGeometry):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def length(self):
        pass
    
# TODO need to make sure there's no intersection or loops; this should probably be checked in __new__
class Path(Curve):
    def __init__(self, coords): # if ref_point==None, use coords[0] as the center
        self.points = PointCollection(coords)
        self._path_length = None
        self.nedges = self.points.npoints-1
        if self.nedges < 1:
            raise ValueError(f"Cannot define Path with fewer than 2 points, {self.points.npoints} provided")
            
    def translate(self, vector):
        self.points.translate(vector)
            
    def rotate(self, axis, location=None):
        self.points.rotate(axis, location)
        
    def reflect(self, plane):
        self.points.reflect(plane)
        
    def scale(self, vector, location=None):
        self.points.scale(vector, location)
        self._path_length.clear()
    
    def shear(self):
        raise NotImplementedError("shearing a path not yet implemented")
        self.points.shear()
        self._path_length.clear()
        
    def draw(self, ax, *args, **kwargs):
        # TODO really should not be accessing points.points directly. Should try to use the self.points[] syntax
        ax.plot3D(self.points.points[:,0], self.points.points[:,1], self.points.points[:,2], *args, **kwargs)
        
    def length(self):
        if self._path_length is None:
            self._path_length = np.cumsum([self.points.point_distance(i, i+1) for i in range(self.nedges)])
        return self._path_length[-1]
    
class ClosedPath(Path):
    def __init__(self, coords):
        if len(coords) > 1 and utils.is_iterable(coords[0]):
            coords = list(coords)
            while len(coords) > 1 and coords[0] == coords[-1]:
                coords.pop()

        if len(coords) <= 1 or not utils.is_iterable(coords[0]):
            raise ValueError(f"Cannot initialize ClosedPath with fewer than 2 points convertible to numpy arrays: {coords}")
        super().__init__(coords)
        self.nedges = self.points.npoints # override definition of self.nedges from Path
        
    def draw(self, ax, *args, **kwargs):
        # TODO really should not be accessing points.points directly. Should try to use the self.points[] syntax
        ax.plot3D(self.points.points[:,0].tolist() + [self.points[0,0]], 
                  self.points.points[:,1].tolist() + [self.points[0,1]], 
                  self.points.points[:,2].tolist() + [self.points[0,2]], 
                  *args, **kwargs)
        
    # override length calculation and self._path_length from Path
    def length(self):
        if self._path_length is None:
            self._path_length = np.cumsum([self.points.point_distance(i, i+1) for i in range(self.nedges-1)] + [self.points.point_distance(0, self.nedges-1)])
        return self._path_length[-1]
    
CIRCLE_MIN_PTS = 8
def circle_error(npoints, q='length'):
    if q == 'length':
        factor = 1.0
    elif q == 'area':
        factor = 2.0
    else:
        raise ValueError(f"invalid value in circle_error: {q} provided but must be 'length' or 'area'")
    return 1-npoints/factor/np.pi*np.sin(factor*np.pi/npoints)
    
# create a circle
# possible values for npoints:
#   'length' - cost function is length error (default)
#   'area' - cost function is error in area
#   [integer] - use the provided value
def circle(radius, location=None, orientation=None, npoints=None, fill=False, optimizer = lambda N, err: N[-1]+1, tol=DEF_OPTIMIZER_PRECISION, coords_only=False):
    if npoints is None:
        npoints = partial(circle_error, q=('area' if fill else 'length'))
    if callable(npoints):
        N = [CIRCLE_MIN_PTS]
        err = [npoints(N[-1])]
        while err[-1] > tol:
            N.append(optimizer(N, err))
            err.append(npoints(N[-1]))
        j = len(err)-1
        while j>=0 and err[-1] > tol:
            j -= 1
        npoints = N[j]
        
    elif type(npoints)!=int:
        raise ValueError("invalid value in circle function for argument npoints")
      
    dtheta = 2*np.pi/npoints
    theta = np.linspace(0, (npoints-1)*dtheta, npoints)
    coords = []
    for i in range(npoints):
        coords.append([radius*np.cos(theta[i]), radius*np.sin(theta[i]),0])
    
    obj = ClosedPath(coords)
    if not orientation is None:
        obj.rotate(orientation_to_rotation(format_as_points(orientation)), [0,0,0])
    if not location is None:
        obj.translate(format_as_points(location))
        
    if coords_only:
        raise NotImplementedError("returning coords from circle is not yet implemented")
    return obj

ELLIPSE_MIN_PTS = 8
def ellipse(major_radius, minor_radius, location=None, orientation=None, npoints=None, fill=False, optimizer = lambda N, err: N[-1]+1, tol=DEF_OPTIMIZER_PRECISION, coords_only=False):
    if npoints is None:
        # TODO: optimizer features not yet implemented
        raise NotImplementedError("must specify a number of points for ellipse...optimizers not yet implemented")
    if callable(npoints):
        raise NotImplementedError("must specify a number of points for ellipse...optimizers not yet implemented")
    elif type(npoints)!=int:
        raise ValueError("invalid value in circle function for argument npoints")
    
    # this is the 
    # TODO: when an optimizer is implemented, this should change
    dtheta = 2*np.pi/npoints
    theta = np.linspace(0, (npoints-1)*dtheta, npoints)
    coords = []
    for i in range(npoints):
        coords.append([major_radius*np.cos(theta[i]), minor_radius*np.sin(theta[i]),0])
    
    obj = ClosedPath(coords)
    if not orientation is None:
        obj.rotate(orientation_to_rotation(format_as_points(orientation)), [0,0,0])
    if not location is None:
        obj.translate(format_as_points(location))
    
    if coords_only:
        raise NotImplementedError("returning coords from circle is not yet implemented")
    return obj

# npoints is the number of points per turn
def coil(radius, pitch, nturns, location=None, orientation=None, npoints=None, coords_only=False):
    N = int(nturns*npoints)
    dtheta = 2*np.pi*nturns/N
    theta = np.linspace(0, (N-1)*dtheta, N) # this isn't exactly 
    dz = pitch*nturns/(N-1)
    coords = []
    for i in range(N):
        coords.append([radius*np.cos(theta[i]), radius*np.sin(theta[i]), dz*i])
                       
    obj = Path(coords)
    if not orientation is None:
        obj.rotate(orientation_to_rotation(format_as_points(orientation)), [0,0,0])
    if not location is None:
        obj.translate(format_as_points(location))
    
    if coords_only:
        raise NotImplementedError("returning coords from circle is not yet implemented")
    return obj

#def HelmholtzCoil(radius, location=None, orientation=None)