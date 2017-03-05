"""
File: distances.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""

import numpy as np


def hamming_distance(s1, s2):
    if s1.shape != s2.shape:
        raise ValueError("Undefined for sequence of unequal length")
    return np.sum(s1 != s2)


def manhattan_distance(s1, s2):
    if s1.shape != s2.shape:
        raise ValueError("Undefined for sequence of unequal length")
    return np.linalg.norm(s1 - s2, ord=1)


def euclidian_distance(s1, s2):
    if s1.shape != s2.shape:
        raise ValueError("Undefined for sequence of unequal length")
    return np.linalg.norm(s1 - s2, ord=2)
