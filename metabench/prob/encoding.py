"""
File: encoding.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Describe how to represent a solution.
"""

import math

import numpy as np

import metabench.misc.distances as dist


class Solution(np.ndarray):
    """Represent a potential solution to a problem.

    Args:
        input_array (np.ndarray): Holds the values of the solution.
        encoding (Encoding): The encoding of the solution.

    Attributes:
        encoding (Encoding): The encoding of the solution.

    """
    def __new__(cls, input_array, encoding):
        obj = np.asarray(input_array).view(cls)
        obj.encoding = encoding
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._encoding = getattr(obj, 'encoding', None)

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        self._encoding = encoding


class Encoding(object):
    """Abstract class for the encodings."""

    def distance(self, solution_1, solution_2):
        """Get the distance between two solutions arrays.

        These solution arrays must be of the proper encoding.

        Args:
            solution_1 (Solution): First array.
            solution_2 (Solution): Second array.

        Returns:
            float: the distance between the two solutions arrays.

        """
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
            the dist.hamming_distance.

    Attributes:
        size (int): Size of the solution array.
        distance (func): Distance function used between solutions.

    """
    def __init__(self, size, distance=dist.hamming_distance):
        super().__init__()
        if size <= 0:
            raise ValueError('Cannot encode solution on an array of negative'
                             ' or empty size')
        self.size = size
        self.distance = distance

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
    def __init__(self, boundaries, distance=dist.manhattan_distance):
        super().__init__()
        self.boundaries = boundaries
        self.size = len(boundaries)
        self.distance = distance

    def generate_random_solution(self):
        values = []
        for i in range(self.size):
            values.append(np.random.randint(self.boundaries[i][0],
                                            self.boundaries[i][1]))
        solution = Solution(np.array(values, np.int), self)
        return solution

    def space_size(self):
        space_size = 1.
        for i in range(self.size):
            space_size *= (self.boundaries[i][1] - self.boundaries[i][0])
        return space_size


class RealVector(Encoding):
    def __init__(self, boundaries, distance=dist.euclidian_distance):
        super().__init__()
        self.boundaries = boundaries
        self.distance = distance

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
        super().__init__()
        self.boundaries = boundaries
        self.types = types

    def generate_random_solution(self):
        sol = []
        for i in range(len(self.boundaries)):
            if self.types[i] is bool:
                sol.append(np.random.randint(2))
            elif self.types[i] is int:
                sol.append(np.random.randint(self.boundaries[i][0],
                                             self.boundaries[i][1]))
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
