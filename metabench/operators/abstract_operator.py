"""
File: abstract_operator.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Abstract operator.
"""

from enum import Enum


class OperatorType(Enum):
    NEIGHBORHOOD = 'Neighborhood'


class AbstractOperator(object):
    """Abstract class describing an operator.

    An operator is responsible for generating new solution from one or several
    base solutions.

    Args:
        move_range (MoveRange): Define the step range for the operator function.
            Default is None in the case no MoveRange is required for the
            operator.

    Attributes:
        op_type (OperatorType): type of the operator.
        move_range (MoveRange): Define the step range for the operator function.

    """
    op_type = None

    def __init__(self, move_range=None):
        self.move_range = move_range

    def __call__(self, *solutions, step=None):
        """Generate new solutions from the given base solutions.

        Args:
            solutions (list[Solution]): Base solution that will be used to
                generate the new solutions.
            step (float): Normalized step given by the metaheuristic. Strictly
                between 0.0 and 1.0. Default is None in case no step is required
                by the operator.

        Yield:
            Solution: created from the given solutions.
            Modifs: the modifications made on the solution to create the new
                solution.

        """
        raise NotImplementedError('Abstract Class')

    def _convert_step(self, step):
        """Convert the normalized step in a value defined by the move range.

        Args:
            step (float): Normalized step given by the metaheuristic. Strictly
                between 0.0 and 1.0.

        Returns:
            int or float: step as defined by the MoveRange or None if the
                operator as no move range defined.

        """
        if self.move_range:
            return self.move_range.convert(step)
        return None
