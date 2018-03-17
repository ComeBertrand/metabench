"""
File: neighborhood_generator.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Operators that create neighbors for a solution.
"""

import numpy as np


class NeighborhoodGenerator(object):
    """Compute the neighborhood for the solutions.

    Args:
        move (func): Move function that has to take a solution as its first
            argument, and return a Solution and a Modifs.
        move_range (MoveRange): Define the step range for the move function.
        max_nb_neighbors (int): Maximum number of neighbors that will be
            computed by a call to the neighborhood.

    Attributes:
        move (func): Move function that has to take a solution as its first
            argument, and return a Solution and a Modifs.
        move_range (MoveRange): Define the step range for the move function.
        max_nb_neighbors (int): Maximum number of neighbors that will be
            computed by a call to the neighborhood.

    Example:
        >>> encoding = BinaryEncoding(10)
        >>> solution = encoding.generate_random_solution()
        >>> solution
        Solution([0, 0, 0, 0, 1, 0, 0, 0, 1, 0])
        >>> neighborhood = Neighborhood(move_binary_flip,
        ... DiscreteMoveRange(1, 2), 5)
        >>> for neighbor, modifs in neighborhood(solution, 0.0):
        ...     print(neighbor)
        ...
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 1]
        [0, 0, 0, 0, 1, 1, 0, 0, 1, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        [0, 0, 0, 1, 1, 0, 0, 0, 1, 0]

    """
    def __init__(self, move, move_range, max_nb_neighbors):
        self.move = move
        self.move_range = move_range
        self.max_nb_neighbors = max_nb_neighbors

    def __call__(self, solution, step):
        """Compute the neighbors of a solution.

        Args:
            solution (Solution): Solution for which the neighbors must be
                computed.
            step (float): Normalized step given by the metaheuristic. Strictly
                between 0.0 and 1.0.

        Yield:
            Solution: neighbors to the given solution.
            Modifs: the modifications made on the solution to create the
                neighbor.

        """
        converted_step = self.move_range.convert(step)
        # TODO: remove the nb_neighbors from the move functions. Moves shall
        # be atomic and just make a modification on a solution and return a
        # neighbor and a modification. They shall probably have a state that
        # prevent them from returning twice the same solution, but that's all.
        for neighbor, modifs in self.move(solution,
                                          converted_step,
                                          self.max_nb_neighbors):
            yield neighbor, modifs
