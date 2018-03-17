"""
File: move_functions.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Move functions for space discovery.
"""

from itertools import combinations, product
from enum import Enum

import numpy as np

from ...utils import implemented_for
from ...common.fitness import Modifs


@implemented_for('BinaryEncoding')
def move_binary_flip(solution, step):
    """Compute the neighbors of binary encoded solution by flipping bits.

    Args:
        solution (Solution): The solution for which neighbors are generated.
        step (int): Number of bits to be flipped to create the neighbors.
            Strictly positive.

    Returns:
        Solution: neighbor.
        Modifs: The modifications from given solution to neighbor.

    """
    flip_indexes = np.random.choice(len(solution), size=step, replace=False)
    # The fitness is copied to allow partial fitness computation
    neighbor = solution.copy(copy_fitness=True)
    modifs = Modifs()

    for flip_index in flip_indexes:
        if neighbor[flip_index]:
            neighbor[flip_index] = 0
            modifs.add_modif(flip_index, 1, 0)
        else:
            neighbor[flip_index] = 1
            modifs.add_modif(flip_index, 0, 1)

    return neighbor, modifs


@implemented_for('RealEncoding')
def move_distance_continuous(solution, step):
    """Compute the neighbor of real-encoded solution.

    Neighbor will be randomly taken on the hypersphere of center 'solution'
    and radius 'step'.

    Args:
        solution (Solution): The solution for which neighbors are generated.
        step (float): Radius of the hypersphere.

    Returns:
        Solution: neighbor.
        Modifs: The modifications from given solution to neighbor.

    """
    vector = np.random.normal(0, 1, len(solution))
    vector /= np.linalg.norm(vector)
    vector *= step
    neighbor = solution.copy()
    neighbor += vector
    neighbor.to_bounds()

    # Modifs is empty, since all attributes of the neighbor might be
    # modified. (Empty modifs means full fitness must be re-computed).
    modifs = Modifs()
    return neighbor, modifs


@implemented_for('DiscreteEncoding')
def move_substitution(solution, step):
    """Create neighbor for solutions with a discrete encoding.

    Neighbor is created by substituting the value of one of the attribute by
    another allowed value.

    Args:
        solution (Solution): The solution for which neighbors are generated.
        step (int): Number of substitution to make. Strictly positive.

    Returns:
        Solution: neighbor.
        Modifs: The modifications from given solution to neighbor.

    """
    substitution_indexes = np.random.choice(len(solution), size=step, replace=False)
    neighbor = solution.copy(copy_fitness=True)
    modifs = Modifs()
    for substitution_index in substitution_indexes:
        allowed_values = set(range(solution.min_val(substitution_index),
                                   solution.max_val(substitution_index) + 1))
        allowed_values.remove(solution[substitution_index])
        new_value = np.random.choice(allowed_values, size=1)
        neighbor[substitution_index] = new_value
        modif.add_modif(substitution_index, solution[substitution_index], new_value)

    return neighbor, modif


@implemented_for('PermutationEncoding')
def move_swap(solution, step):
    """Create neighbor for solutions with a permutation encoding.

    The swap move consists in exchanging the value of two index.

    Args:
        solution (Solution): The solution for which neighbors are generated.
        step (int): Number of swaps to make. Strictly positive.

    Returns:
        Solution: neighbor.
        Modifs: The modifications from given solution to neighbor.

    """
    # TODO: check for ValueError if the length of the solution is too small and
    # step is too high
    swaps = np.random.choice(len(solution), size=(step, 2), replace=False)

    neighbor = solution.copy(copy_fitness=True)
    modif = Modifs()

    for index_1, index_2 in swaps:
        neighbor[index_1] = solution[index_2]
        neighbor[index_2] = solution[index_1]
        modif.add_modif(index_1, solution[index_1], neighbor[index_1])
        modif.add_modif(index_2, solution[index_2], neighbor[index_2])

    return neighbor, modif


@implemented_for('PermutationEncoding')
def move_opt(solution, step):
    raise NotImplementedError("TODO")


@implemented_for('PermutationEncoding')
def move_insertion(solution, step):
    raise NotImplementedError("TODO")


@implemented_for('PermutationEncoding')
def move_inversion(solution, step):
    raise NotImplementedError("TODO")


class MoveFunctionsEnum(Enum):
    BINARY_FLIP = move_binary_flip
    DISTANCE_CONTINUOUS = move_distance_continuous
    SUBSTITUTION = move_substitution
    SWAP = move_swap
