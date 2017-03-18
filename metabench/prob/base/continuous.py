"""
File: continuous.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Classical continuous functions for performance evaluation of
metaheuristics.
"""

from functools import partial

import numpy as np

from metabench.prob.problem import Problem
from metabench.prob.encoding import RealEncoding, Boundaries
from metabench.prob.objective import Objective
from metabench.prob.operators.neighborhood import move_distance_continuous


def sphere_func(solution):
    """Sphere function."""
    return np.sum(solution * solution)


class Sphere(Problem):
    """Sphere problem.

    Args:
        n_dim (int): Number of dimensions.
        min_val (float): Lower bound of each dimensions.
        max_val (float): Upper bound of each dimensions.

    """
    def __init__(self, n_dim, min_val, max_val):
        step = max_val - min_val / 1000.
        neighborhood = partial(move_distance_continuous, step=step,
                               nb_neighbors=n_dim*100)
        boundaries = Boundaries(np.array([min_val]*n_dim, np.float),
                                np.array([max_val]*n_dim, np.float),
                                np.float)
        encoding = RealEncoding(boundaries)
        objective = Objective(sphere_func)
        super().__init__(objective, encoding, neighborhood=neighborhood)
