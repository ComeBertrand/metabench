"""
File: solutions.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Wrapper for the candidate solutions.
"""


import numpy as np


class Solution(np.ndarray):
    """Represent a potential solution to a problem.

    Args:
        input_array (np.ndarray): Holds the values of the solution.
        encoding (Encoding): The encoding of the solution.

    Attributes:
        encoding (Encoding): The encoding of the solution.
        fitness (float): The fitness of the solution.

    """
    def __new__(cls, input_array, encoding, fitness=None):
        obj = np.asarray(input_array).view(cls)
        obj.encoding = encoding
        obj.fitness = fitness
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._encoding = getattr(obj, 'encoding', None)
        self._fitness = getattr(obj, 'fitness', None)

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        self._encoding = encoding

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, fitness):
        self._fitness = fitness

    def copy(self, copy_fitness=False):
        """Copy the solution.

        Encoding is always copied, fitness may or may not.

        Args:
            copy_fitness (bool): If True, the fitness will also be copied. Else
                the copy will have no fitness.

        Returns:
            Solution: a copy of itself.

        """
        if copy_fitness:
            return Solution(super().copy(),
                            self.encoding,
                            self.fitness)
        return Solution(super().copy(),
                        self.encoding)

    def max_val(self, index):
        """Find the maximum value that can be taken on a particular index.

        Args:
            index (int): The index for which we want to know the maximum value
                authorized.

        Returns:
            int/float/None: The maximum value authorized or None if there is no
                boundaries on the solution encoding.

        """
        if self.encoding.boundaries is None:
            return None
        return self.encoding.boundaries.max_val(index)

    def max_vals(self):
        """Give all the maximum values that can be taken by a solution.

        Returns:
            np.array or None: array of int/float, all the maximums of the
                attributes, or None if there is no boundaries on the solution
                encoding.

        """
        if self.encoding.boundaries is None:
            return None
        return self.encoding.boundaries.max_vals()

    def min_val(self, index):
        """Find the minimum value that can be taken on a particular index.

        Args:
            index (int): The index for which we want to know the minimum value
                authorized.

        Returns:
            int/float/None: The minimum value authorized or None if there is no
                boundaries on the solution encoding.

        """
        if self.encoding.boundaries is None:
            return None
        return self.encoding.boundaries.min_val(index)

    def min_vals(self):
        """Give all the minimum values that can be taken by a solution.

        Returns:
            np.array or None: array of int/float, all the minimums of the
                attributes, or None if there is no boundaries on the solution
                encoding.

        """
        if self.encoding.boundaries is None:
            return None
        return self.encoding.boundaries.min_vals()

    def to_bounds(self):
        """Set the attributes value of the solution to the min/max bounds."""
        np.copyto(self, np.minimum(self.max_vals(), self))
        np.copyto(self, np.maximum(self.min_vals(), self))
