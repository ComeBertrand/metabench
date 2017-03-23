"""
File: encoding.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Solution encoding and generation in a defined space.
"""

import math
from functools import reduce

import numpy as np

from metabench.prob.solution import Solution


class Boundaries(np.ndarray):
    """Represent the limit of the space for the attribute of a solution.

    A boundaries records the minimum and maximum values that a solution
    can take for each of its attribute.
    These values may be of any numeric type (int or float).

    Boundaries can also be used to normalize a solution vector, so that
    distance computation is accurate.

    Boundaries have always the same shape, it is a matrix of 3 lines and
    n columns (n being the number of attribute of the solutions).
    - The 1st line records the minimum values for the attributes (included).
    - The 2nd line records the maximum values for the attributes (included).
    - The 3td line records the difference between the maximum and the
    minimum values. This is the space size of each attribute used for
    the normalization of solution vectors.

    Of course, for a specific attribute the minimum value must always be
    lower or equal to the maximum value.

    Args:
        minimums (list): of minimum values.
        maximums (list): of maximum values.
        type (type): type of the values, default is np.int.

    Returns:
        np.array: of shape (3, n), n being the size of the minimums/maximums
            vectors.

    """
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

        # Add epsilon to avoid division per 0 when max == min during
        # normalization.
        epsilon = np.finfo(np.float).resolution
        bounds = np.array([minimums,
                           maximums,
                           (maximums-minimums) + epsilon],
                          type)
        obj = np.asarray(bounds).view(cls)
        return obj

    def max_val(self, index):
        """Get the maximum value authorized for an index."""
        return self.__getitem__((1, index))

    def max_vals(self):
        """Get all the maximum values authorized for the attributes."""
        return self.__getitem__(1)

    def min_val(self, index):
        """Get the minimum value authorized for an index."""
        return self.__getitem__((0, index))

    def min_vals(self):
        """Get all the minimum values authorized for the attributes."""
        return self.__getitem__(0)

    def normalize(self, array):
        """Normalize an array according to the space size of its attributes.

        Normally used on the difference between two solution to compute
        an accurate distance.

        Args:
            array (np.array): array to be normalized.

        Returns:
            np.array: normalized array.

        """
        return array / self.__getitem__(2)


class Encoding(object):
    """Abstract class for the encodings.

    An encoding is a manner of representing a candidate solution. It will
    have an impact on the type of information is it supposed to represent
    as well as the operators that can be applied to create/change/select
    candidate solutions.

    The role of an encoding is to keep information about the space on which
    the solution can be create and the constraint on it.

    It is also used to compute statistics on the solution space.

    Args:
        boundaries (Boundaries): Boundaries on the solution space. Default is
            None.
        ord (int): Order of the norm used for distance computation (if a
            distance is defined on the solution space). Default is None.

    Attributes:
        boundaries (Boundaries): Boundaries on the solution space.
        ord (int): Order of the norm used for distance computation (if a
            distance is defined on the solution space).

    """
    def __init__(self, boundaries=None, ord=None):
        self.boundaries = boundaries
        self.ord = ord

    def generate_random_solution(self):
        """Generate a random candidate solution.

        Returns:
            Solution: A random solution array.

        """
        raise NotImplementedError('Abstract Class')

    def space_size(self):
        """Compute the size of the solution space defined by the encoding.

        Returns:
            int: the space size.

        """
        raise NotImplementedError('Abstract Class')

    def distance(self, solution_1, solution_2):
        """Get the distance between two candidate solutions arrays.

        These solution arrays must be of the proper encoding.

        The difference between two solution arrays will be normalized if
        boundaries are defined on the solution space.

        Args:
            solution_1 (Solution): First array.
            solution_2 (Solution): Second array.

        Returns:
            float: the distance between the two solutions arrays.

        """
        if self.ord is None:
            raise NotImplementedError('No distance is given to this encoding')

        if solution_1.encoding != self or solution_2.encoding != self:
            raise ValueError('{0.__class__.__name__} can only compute distance'
                             ' between solutions that are encoded with '
                             'itself.'.format(self))

        diff = solution_1 - solution_2
        if self.boundaries:
            diff = self.boundaries.normalize(diff)

        return np.linalg.norm(diff, ord=self.ord)


class BinaryEncoding(Encoding):
    """Encode a solution as an array of binary values.

    The norm used to compute distances in the solution space is the hamming
    distance (norm of order 0).

    Args:
        size (int): Size of the solution array. Must be positive.

    Attributes:
        size (int): Size of the solution array.

    """
    def __init__(self, size):
        if size <= 0:
            raise ValueError('Cannot encode solution on an array of negative'
                             ' or empty size')

        b = Boundaries(np.zeros(size), np.zeros(size) + 1, type=np.int)
        super().__init__(boundaries=b, ord=0)

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
        return 2 ** self.size


class DiscreteEncoding(Encoding):
    """Encode a solution as an array of integer values.

    The norm used to compute distances in the solution space is the manhattan
    distance (norm of order 1).

    Args:
        boundaries (Boundaries): Boundaries on the solution space, must be of
            type int.

    """
    def __init__(self, boundaries):
        if not boundaries.dtype == np.int:
            raise TypeError("The boundaries of a discrete encoding must be of"
                            " type int")
        super().__init__(boundaries, ord=1)

    def generate_random_solution(self):
        """Generate a random solution.

        Randomly create an integer array with uniform distribution on the
        solution space of each index.

        Returns:
            Solution: A random solution array.

        """
        values = np.zeros(self.boundaries.shape[1], np.int)
        for i in range(self.boundaries.shape[1]):
            values[i] = np.random.random_integers(self.boundaries[0][i],
                                                  self.boundaries[1][i])
        solution = Solution(values, self)
        return solution

    def space_size(self):
        space_size = reduce(lambda x, y: x*y, self.boundaries[2] + 1)
        return space_size


class RealEncoding(Encoding):
    """Encode a solution as an array of float values.

    The norm used to compute distances in the solution space is the euclidian
    distance (norm of order 2).

    Args:
        boundaries (Boundaries): Boundaries on the solution space. Must be of
            type float.

    """
    def __init__(self, boundaries):
        if not boundaries.dtype == np.float:
            raise TypeError("The boundaries of a real encoding must be of"
                            " type float")
        super().__init__(boundaries, ord=2)

    def generate_random_solution(self):
        """Generate a random solution.

        Randomly create an integer array with uniform distribution on the
        solution space of each index.

        Returns:
            Solution: A random solution array.

        """
        values = np.zeros(self.boundaries.shape[1], np.float)
        for i in range(self.boundaries.shape[1]):
            values[i] = np.random.uniform(self.boundaries[0][i],
                                          self.boundaries[1][i])
        solution = Solution(values, self)
        return solution


class PermutationEncoding(Encoding):
    """Encode a solution as permutation of a list of items.

    No distance is defined on the solution space of the permutations.

    Args:
        items (list): Items that will be permuted.

    Attributes:
        items (np.array): Items that will be permuted.

    """
    def __init__(self, items):
        super().__init__()
        self.items = np.array(items)

    def generate_random_solution(self):
        """Generate a random solution.

        Randomly create a permutation of the items.

        Returns:
            Solution: A random solution array.

        """
        values = np.array(self.items, copy=True)
        np.random.shuffle(values)
        solution = Solution(values, self)
        return solution

    def space_size(self):
        return math.factorial(len(self.items))


class MixedEncoding(Encoding):
    """TODO: work on this to make work with numpy arrays"""
    def __init__(self):
        raise NotImplementedError("TODO")
