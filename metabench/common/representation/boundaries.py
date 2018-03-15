"""
File: boundaries.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Boundaries of solution space.
"""

import numpy as np


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
            np.array: normalized array.

        """
        return array / self.__getitem__(2)
