"""
File: abstract.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: A problem describe a function or an instance that needs to be
optimized.
"""

from ..common.solution import Solution


class Problem(object):
    """Problem to be solved by a Metaheuristic.

    The role of the problem is to describe the potential solutions, generate
    them and evaluate them.
    It also provide the operators to modify them.

    Args:
        objective (Objective): The objective (or fitness) function to optimize.
        encoding (Encoding): The encoding of the candidate solutions.
        known_min (float): Known minimum of the fitness for the problem. If it
            is not known, set to None. Default is None.
        neighborhood (Neighborhood): Neighborhood operator that can be used to
            find neighboring candidate solutions for a given solution. Default
            is None.

    Attributes:
        objective (Objective): The objective (or fitness) function to optimize.
        encoding (Encoding): The encoding of the candidate solutions.
        neighborhood (Neighborhood): Neighborhood operator that can be used to
            find neighboring candidate solutions for a given solution.

    """
    def __init__(self, objective, encoding, known_min=None, neighborhood=None):
        self.objective = objective
        self.encoding = encoding
        self.known_min = known_min
        self.neighborhood = neighborhood

    def evaluate(self, solution, modifs=None):
        """Evaluate the fitness of a solution.

        The evaluation can be partial if the modifs that lead to its creation
        are given (and if the objective given at the initialization own a
        partial fitness function).

        Args:
            solution (Solution): solution to be evaluated.
            modifs (Modifs): modifications that were made on the solution
                to create it.

        """
        self.objective(solution, modifs)

    def generate_solution(self):
        """Generate a random solution.

        Returns:
            Solution

        """
        return Solution(self.encoding.generate_random_value(), self.encoding)

    def get_neighbors(self, solution, step):
        """Generate the neighbors of a given solution.

        Args:
            solution (Solution): solution for which we want to create
                neighbors.
            step (float): Normalized step given by the metaheuristic. Strictly
                between 0.0 and 1.0.

        Yield:
            Solution: the neighboring solutions.
            Modifs: the modifications made to the solution to create the
                neighbor.

        Raises:
            NotImplementedError: if no Neighborhood was given at the problem
                creation.

        """
        if self.neighborhood is not None:
            for neighbor, modifs in self.neighborhood(solution, step):
                yield neighbor, modifs
        else:
            raise NotImplementedError('No neighborhood operator is implemented'
                                      ' for this problem.')
