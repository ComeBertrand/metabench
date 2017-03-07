"""
File: distances.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""

import numpy as np


def sol_distance(s1, s2, boundaries=None, ord=2):
    if s1.shape != s2.shape:
        raise ValueError("Undefined for sequence of unequal length")
    if boundaries is None:
        return np.linalg.norm(s1 - s2, ord=ord)

    if s1.encoding.boundaries != boundaries:
        raise ValueError("Given boundaries do not apply to the solutions")

    return np.linalg.norm(boundaries.relativize(s1 - s2), ord=ord)
