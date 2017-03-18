"""
File: objective.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""

import numpy as np


class Objective(object):
    def __init__(self, fitness, fitness_partial=None):
        self.fitness = fitness
        self.fitness_partial = fitness_partial

    def __call__(self, solution, *moves):
        if solution.fitness is None:
            if moves and self.fitness_partial:
                solution.fitness = self.fitness_partial(solution, *moves)
            else:
                solution.fitness = self.fitness(solution)


class ObjectiveNoisy(object):
    """TODO"""
    def __init__(self, fitness, std, fitness_partial=None):
        super().__init__(fitness, fitness_partial)
        self.std = std

    def __call__(self, solution, *moves):
        val = super().__call__(solution, *moves)
