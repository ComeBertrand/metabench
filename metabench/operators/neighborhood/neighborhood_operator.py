"""
File: neighborhood_generator.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Operators that create neighbors for a solution.
"""

import numpy as np

from .move_functions import MoveFunctionsEnum
from .move_range import ContinuousMoveRange, ContinuousLogMoveRange, DiscreteMoveRange, DiscreteLogMoveRange
from ..abstract_operator import AbstractOperator, OperatorType


def neigborhood_factory(move_function_enum, min_range, max_range, log_range=False, max_nb_neighbors=1):
    if move_function_enum == MoveFunctionsEnum.DISTANCE_CONTINUOUS:
        if log_range:
            move_range = ContinuousLogMoveRange(float(min_range), float(max_range))
        else:
            move_range = ContinuousMoveRange(float(min_range), float(max_range))
    else:
        if log_range:
            move_range = DiscreteLogMoveRange(int(min_range), int(max_range))
        else:
            move_range = DiscreteMoveRange(int(min_range), int(max_range))

    return NeighborhoodOperator(move_function_enum.value, move_range, max_nb_neighbors)


class NeighborhoodOperator(AbstractOperator):
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
    op_type = OperatorType.NEIGHBORHOOD

    def __init__(self, move, move_range, max_nb_neighbors):
        super().__init__(move_range)
        self.move = move
        self.max_nb_neighbors = max_nb_neighbors

    def __call__(self, solution, step=0.):
        """Compute the neighbors of a solution.

        Args:
            solution (Solution): Solution for which the neighbors must be
            step (float): Normalized step given by the metaheuristic. Strictly
                between 0.0 and 1.0.

        Yield:
            Solution: neighbors to the given solution.
            Modifs: the modifications made on the solution to create the
                neighbor.

        """
        converted_step = self._convert_step(step)
        seen_modifs = set()
        for _ in range(self.max_nb_neighbors):
            result = None
            while result is None:
                neighbor, modif = self.move(solution, converted_step)
                if not modif or modif not in seen_modifs:
                    seen_modifs.add(modif)
                    result = (neighbor, modif)
            yield result
