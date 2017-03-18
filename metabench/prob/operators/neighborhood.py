"""
File: neighborhood.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""

import numpy as np

from metabench.misc.decorator import not_implemented_for, implemented_for


class Neighborhood(object):
    def __init__(self, move):
        self.move = move

    def __call__(self, solution, **parameters):
        for neighbor in self.move(solution, **parameters):
            yield neighbor


@implemented_for('BinaryEncoding')
def move_binary_flip(solution):
    indexes = np.array(range(len(solution)))
    np.random.shuffle(indexes)
    for index in indexes:
        neighbor = solution.copy()
        if neighbor[index]:
            neighbor[index] = 0
        else:
            neighbor[index] = 1
        yield neighbor


@implemented_for('RealEncoding')
def move_distance_continuous(solution, step):
    indexes = np.array(range(len(solution)))
    np.random.shuffle(indexes)
    for index in indexes:
        for direction in [-1., 1.]:
            neighbor = solution.copy()
            new_val = neighbor[index] + direction * step
            if neighbor.min_val(index) <= new_val <= neighbor.max_val(index):
                neighbor[index] = new_val
                yield neighbor


@implemented_for('DiscreteEncoding')
def move_substitution(solution):
    indexes = np.array(range(len(solution)))
    np.random.shuffle(indexes)
    for index in indexes:
        allowed_values = set(range(solution.min_val(index),
                                   solution.max_val(index)))
        allowed_values.remove(solution[index])
        for val in allowed_values:
            neighbor = solution.copy()
            neighbor[index] = val
            yield neighbor


@implemented_for('PermutationEncoding')
def move_swap(solution):
    len_sol = len(solution)
    for i in range(len_sol - 1):
        for j in range(i+1, len_sol):
            neighbor = solution.copy()
            neighbor[i] = solution[j]
            neighbor[j] = solution[i]
            yield neighbor


@implemented_for('PermutationEncoding')
def move_2opt(solution):
    pass


@implemented_for('PermutationEncoding')
def move_insertion(solution):
    pass


@implemented_for('PermutationEncoding')
def move_inversion(solution):
    pass
