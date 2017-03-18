"""
File: solutions.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
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
        if copy_fitness:
            return Solution(super().copy(),
                            self.encoding,
                            self.fitness)
        return Solution(super().copy(),
                        self.encoding)

    def max_val(self, index):
        if self.encoding.boundaries is None:
            return None
        return self.encoding.boundaries.max_val(index)

    def min_val(self, index):
        if self.encoding.boundaries is None:
            return None
        return self.encoding.boundaries.min_val(index)
