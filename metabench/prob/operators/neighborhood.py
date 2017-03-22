"""
File: neighborhood.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Operators that create neighbors for a solution.
"""

import numpy as np

from metabench.misc.decorators import implemented_for
from metabench.prob.objective import Modifs


class Neighborhood(object):
    """Compute the neighborhood for the solutions.

    Args:
        move (func): Move function that has to take a solution as its first
            argument, and return a Solution and a Modifs.

    Attributes:
        move (func): Move function that has to take a solution as its first
            argument, and return a Solution and a Modifs.

    """
    def __init__(self, move):
        self.move = move

    def __call__(self, solution, **parameters):
        """Compute the neighbors of a solution.

        Args:
            solution (Solution): Solution for which the neighbors must be
                computed.
            parameters (dict): parameters to be given to the move function.

        Yield:
            Solution: neighbors to the given solution.
            Modifs: the modifications made on the solution to create the
                neighbor.

        """
        for neighbor, modifs in self.move(solution, **parameters):
            yield neighbor, modifs


@implemented_for('BinaryEncoding')
def move_binary_flip(solution):
    """Compute the neighbors of binary encoded solution by flipping a bit."""
    indexes = np.array(range(len(solution)))
    np.random.shuffle(indexes)
    for index in indexes:
        neighbor = solution.copy(True)
        modifs = Modifs()
        if neighbor[index]:
            neighbor[index] = 0
            modifs.add_modif(index, 1, 0)
        else:
            neighbor[index] = 1
            modifs.add_modif(index, 0, 1)
        yield neighbor, modifs


@implemented_for('RealEncoding')
def move_distance_continuous(solution, step, nb_neighbors):
    """Compute the neighbors of real-encoded solution.

    Neighbors will be randomly taken on the hypersphere of center 'solution'
    and radius 'step'.

    Args:
        solution (Solution): The solution for which neighbors are generated.
        step (float): Radius of the hypersphere.
        nb_neighbors (int): Number of neighbors to be generated.

    Yield:
        Solution: neighbors.

    """
    for _ in range(nb_neighbors):
        vector = np.random.normal(0, 1, len(solution))
        vector /= np.linalg.norm(vector)
        vector *= step
        neighbor = solution.copy(True)
        neighbor += vector
        neighbor.to_bounds()

        # Modifs is empty, since all attributes of the neighbor are probably
        # modified.
        modifs = Modifs()
        yield neighbor, modifs


@implemented_for('DiscreteEncoding')
def move_substitution(solution):
    """Create neighbors for solutions with a discrete encoding.

    Neighbors are created by substituting the value of one of the attribute by
    another allowed value. A neighbor will be created for each attribute and
    new possible value.

    Args:
        solution (Solution): The solution for which neighbors are generated.

    Yield:
        Solution: neighbors.

    """
    indexes = np.array(range(len(solution)))
    np.random.shuffle(indexes)
    for index in indexes:
        allowed_values = set(range(solution.min_val(index),
                                   solution.max_val(index)))
        allowed_values.remove(solution[index])
        for val in allowed_values:
            neighbor = solution.copy(True)
            neighbor[index] = val
            modifs = Modifs()
            modifs.add_modif(index, solution[index], val)
            yield neighbor, modifs


@implemented_for('PermutationEncoding')
def move_swap(solution):
    """Create neighbors for solutions with a permutation encoding.

    The swap move consists in exchanging the value of two index. All the swaps
    possible will create the neighborhood for a solution.

    Args:
        solution (Solution): The solution for which neighbors are generated.

    Yield:
        Solution: neighbors.

    """
    len_sol = len(solution)
    for i in range(len_sol - 1):
        for j in range(i+1, len_sol):
            neighbor = solution.copy(True)
            neighbor[i] = solution[j]
            neighbor[j] = solution[i]
            modifs = Modifs()
            modifs.add_modif(i, solution[i], neighbor[i])
            modifs.add_modif(j, solution[j], neighbor[j])
            yield neighbor, modifs


@implemented_for('PermutationEncoding')
def move_2opt(solution):
    raise NotImplementedError("TODO")


@implemented_for('PermutationEncoding')
def move_insertion(solution):
    raise NotImplementedError("TODO")


@implemented_for('PermutationEncoding')
def move_inversion(solution):
    raise NotImplementedError("TODO")
