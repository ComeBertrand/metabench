"""
File: distances.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""

import numpy as np


def sol_distance(s1, s2, normalize=None, ord=2):
    if normalize is None:
        def normalize(array):
            return array

    if s1.shape != s2.shape:
        raise ValueError("Undefined for sequence of unequal length")

    return np.linalg.norm(normalize(s1 - s2), ord=ord)
