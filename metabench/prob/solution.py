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


class MultiSolution(object):
    """Docstring for MultiSolution. """
    def __init__(self):
        """TODO: to be defined1. """
