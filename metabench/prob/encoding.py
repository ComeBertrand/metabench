"""
File: encoding.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Describe how to represent a solution.
"""

import math
from functools import partial

import numpy as np

from metabench.misc.distances import sol_distance
from metabench.prob.solution import Solution


class Boundaries(np.ndarray):
    def __new__(cls, minimums, maximums, type=np.int):
        len_minimums = len(minimums)
        if len_minimums != len(maximums):
            raise ValueError('Length of minimums and maximums are unequal')

        err_indexes = []
        for i in range(len_minimums):
            if maximums[i] < minimums[i]:
                err_indexes.append(i)
        if err_indexes:
            raise ValueError('Maximum bounding values are inferior to the '
                             'minimum bounding value at the following indexes '
                             ': {}'.format(err_indexes))

        epsilon = np.finfo(np.float).epsilon
        bounds = np.array([[x, y, np.max(y-x, epsilon)] for x, y in
                           zip(minimums, maximums)], type)
        obj = np.asarray(bounds).view(cls)
        return obj

    def relativize(self, array):
        return array / np.transpose(self)[2]


class Encoding(object):
    """Abstract class for the encodings."""

    def __init__(self, boundaries=None, distance=None):
        self.boundaries = boundaries
        self.distance = distance

    def distance(self, solution_1, solution_2):
        """Get the distance between two solutions arrays.

        These solution arrays must be of the proper encoding.

        Args:
            solution_1 (Solution): First array.
            solution_2 (Solution): Second array.

        Returns:
            float: the distance between the two solutions arrays.

        """
        if self.distance is None:
            raise NotImplementedError('No distance is given to this encoding')
        if solution_1.encoding != self or solution_2.encoding != self:
            raise ValueError('{0.__class__.__name__} can only compute distance'
                             ' between solutions that are encoded with '
                             'itself.'.format(self))
        return self.distance(solution_1, solution_2)


class BinaryEncoding(Encoding):
    """Encode a solution as an array of binary values.

    Args:
        size (int): Size of the solution array.
        distance (func): Distance function used between solutions. Default is
            None (meaning than the hamming distance will be used (norm 0)).

    Attributes:
        size (int): Size of the solution array.
        distance (func): Distance function used between solutions.

    """
    def __init__(self, size, distance=None):
        if distance is None:
            distance = partial(sol_distance, ord=0)

        super().__init__(distance=distance)

        if size <= 0:
            raise ValueError('Cannot encode solution on an array of negative'
                             ' or empty size')
        self.size = size

    def generate_random_solution(self):
        """Generate a random solution.

        Randomly create a binary array with uniform distribution.

        Returns:
            Solution: A random solution array.

        """
        values = np.random.randint(2, size=self.size)
        solution = Solution(values, self)
        return solution

    def space_size(self):
        """Compute the size of the space defined by the encoding.

        Returns:
            int: the space size.

        """
        return 2 ** self.size


class DiscreteEncoding(Encoding):
    def __init__(self, boundaries, distance=None):
        if distance is None:
            distance = partial(sol_distance,
                               boundaries=boundaries,
                               ord=1)
        super().__init__(boundaries, distance)
        self.size = len(boundaries)

    def generate_random_solution(self):
        values = []
        for i in range(self.size):
            values.append(np.random.random_integers
                          (self.boundaries[i][0], self.boundaries[i][1]))
        solution = Solution(np.array(values, np.int), self)
        return solution

    def space_size(self):
        space_size = 1.
        for i in range(self.size):
            space_size *= (self.boundaries[i][1] - self.boundaries[i][0] + 1)
        return space_size


class RealVector(Encoding):
    def __init__(self, boundaries, distance=None):
        if distance is None:
            distance = partial(sol_distance,
                               boundaries=boundaries,
                               ord=2)
        super().__init__(boundaries, distance)

    def generate_random_solution(self):
        values = []
        for i in range(len(self.boundaries)):
            values.append(np.random.uniform(self.boundaries[i][0],
                                            self.boundaries[i][1]))
        solution = Solution(np.array(values, np.float), self)
        return solution

    def space_size(self):
        return None


class PermutationEncoding(Encoding):
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.size = len(items)

    def generate_random_solution(self):
        values = np.array(self.items)
        np.random.shuffle(values)
        solution = Solution(values, self)
        return solution

    def space_size(self):
        return math.factorial(self.size)

    def distance(self, solution_1, solution_2):
        raise NotImplementedError('Distance functions are not implemented for '
                                  'permutation based solution.')


class MixedEncoding(Encoding):
    """TODO: work on this to make work with numpy arrays"""
    def __init__(self, boundaries, types):
        super().__init__(boundaries)
        self.types = types

    def generate_random_solution(self):
        sol = []
        for i in range(len(self.boundaries)):
            if self.types[i] is bool:
                sol.append(np.random.randint(2))
            elif self.types[i] is int:
                sol.append(np.random.random_integers
                           (self.boundaries[i][0], self.boundaries[i][1]))
            elif self.types[i] is float:
                sol.append(np.random.uniform(self.boundaries[i][0],
                                             self.boundaries[i][1]))
            elif self.types[i] is list:
                sol.append(np.random.choice(self.boundaries[i]))
            elif self.types[i] is str:
                sol.append(np.random.choice(self.boundaries[i]))
            else:
                raise TypeError("Unknown type of variable at index {:d} : \
                                {}".format(i, self.types[i]))
        return sol

    def space_size(self):
        if float in self.types:
            return None

        size = 1.
        for i in range(len(self.boundaries)):
            if self.types[i] is bool:
                size *= 2
            elif self.types[i] is int:
                size *= len(range(self.boundaries[i][0],
                                  self.boundaries[i][1]))
            else:
                size *= len(self.boundaries[i])
        return size
