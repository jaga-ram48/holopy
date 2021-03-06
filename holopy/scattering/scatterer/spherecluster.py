# Copyright 2011-2016, Vinothan N. Manoharan, Thomas G. Dimiduk,
# Rebecca W. Perry, Jerome Fung, Ryan McGorty, Anna Wang, Solomon Barkley
#
# This file is part of HoloPy.
#
# HoloPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HoloPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HoloPy.  If not, see <http://www.gnu.org/licenses/>.

'''
Defines Spheres, a Scatterers scatterer consisting of Spheres

.. moduleauthor:: Vinothan N. Manoharan <vnm@seas.harvard.edu>
'''
# COVERAGE: I think all uncovered code is either unreachable or due likely to be
# refactored away


import numpy as np
import warnings

from .sphere import Sphere
from .composite import Scatterers
from ..errors import OverlapWarning, InvalidScatterer
from ...core.math import cartesian_distance, rotate_points

# default to always warning the user about overlaps.  This can be overriden by
# calling this function again with a different action.
warnings.simplefilter('always', OverlapWarning)

class Spheres(Scatterers):
    '''
    Contains optical and geometrical properties of a cluster of spheres.

    Attributes
    ----------
    spheres : list of Spheres
        Spheres which will make up the cluster

    Notes
    -----
    '''

    def __init__(self, scatterers, warn=True):
        if isinstance(scatterers, Sphere):
            #only one sphere and it's not in a list
            self.scatterers = [scatterers]
        else:
            # make sure all components are spheres
            for s in scatterers:
                if not isinstance(s, Sphere):
                    raise InvalidScatterer(self,
                        "Spheres expects all component " +
                        "scatterers to be Spheres.\n" +
                        repr(s) + " is not a Sphere")
            self.scatterers = scatterers

        if self.overlaps:
            warnings.warn(OverlapWarning(self, self.overlaps))

    @property
    def overlaps(self):
        overlaps = []
        for i, s1 in enumerate(self.scatterers):
            for j in range(i+1, len(self.scatterers)):
                s2= self.scatterers[j]
                try:
                    if cartesian_distance(s1.center, s2.center) < (np.max(s1.r) + np.max(s2.r)):
                        overlaps.append((i, j))
                except:
                    # if the coordinates are not something that we can do
                    # arithmatic on, just pass for now, hopefully the overlap
                    # will be caught later.
                    pass
        return overlaps

    def largest_overlap(self):
        largest = 0
        for i, s1 in enumerate(self.scatterers):
            for j in range(i+1, len(self.scatterers)):
                s2= self.scatterers[j]
                largest = max(largest, (np.max(s1.r) + np.max(s2.r)) -
                                       cartesian_distance(s1.center, s2.center))

        return largest

    def add(self, scatterer):
        if not isinstance(scatterer, Sphere):
            raise InvalidScatterer(self,
                "Spheres expects all component " +
                "scatterers to be Spheres.\n" +
                repr(scatterer) + " is not a Sphere")
        self.scatterers.append(scatterer)

    def guess(self):
        return Spheres([sphere.guess() for sphere in self.scatterers])

    @property
    def n(self):
        return np.array([s.n for s in self.scatterers])
    @property
    def n_real(self):
        return np.array([s.n.real for s in self.scatterers])
    @property
    def n_imag(self):
        return np.array([s.n.imag for s in self.scatterers])
    @property
    def r(self):
        return np.array([s.r for s in self.scatterers])
    @property
    def x(self):
        return np.array([s.x for s in self.scatterers])
    @property
    def y(self):
        return np.array([s.y for s in self.scatterers])
    @property
    def z(self):
        return np.array([s.z for s in self.scatterers])
    @property
    def centers(self):
        return np.array([s.center for s in self.scatterers])

    @property
    def center(self):
        return self.centers.mean(0)

