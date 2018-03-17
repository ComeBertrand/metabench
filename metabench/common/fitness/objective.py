"""
File: objective.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Wrappers for the fitness functions.
"""

from .modif import Modifs


class Objective(object):
    """Wrapper for the fitness functions.

    Fitness will be computed for the given solutions, and put in their
    'fitness' attribute. The wrapper will not return any value when called.

    Args:
        fitness (func): Fitness function that takes a solution and returns a
            fitness value as a float.
        fitness_partial (func): Partial fitness function that can compute a new
            fitness by evaluating the change made by some moves. Default is
            None.

    Attributes:
        fitness (func): Fitness function that takes a solution and returns a
            fitness value as a float.
        fitness_partial (func): Partial fitness function that can compute a new
            fitness by evaluating the change made by some moves. Default is
            None.

    """
    def __init__(self, fitness, fitness_partial=None):
        self.fitness = fitness
        self.fitness_partial = fitness_partial

    def __call__(self, solution, modifs=None):
        """Fill the fitness attribute of a solution.

        The fitness function will only be called if the fitness of the solution
        is None or if moves where made on the solution.

        Args:
            solution (Solution): The solution to evaluate.
            modifs (Modifs): List of modifications made on the solution.
                Default is None.

        """
        if solution.fitness is None or modifs is not None:
            solution.fitness = self._compute_fitness_value(solution, modifs)

    def _compute_fitness_value(self, solution, modifs):
        """Choose which fitness function to use for the fitness computation.

        Args:
            solution (Solution): The solution to evaluate.
            modifs (Modifs): List of modifications made on the solution.

        Returns:
            float: The new fitness for the solution.

        """
        if solution.fitness is not None and modifs and self.fitness_partial:
            return self.fitness_partial(solution, modifs)
        else:
            return self.fitness(solution)


class ObjectiveNoisy(Objective):
    """TODO"""
    def __init__(self, fitness, std, fitness_partial=None):
        super().__init__(fitness, fitness_partial)
        self.std = std

    def __call__(self, solution, modifs):
        super().__call__(solution, modifs)
