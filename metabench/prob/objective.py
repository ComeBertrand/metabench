"""
File: objective.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Wrappers for the fitness functions.
"""


class Objective(object):
    """Wrapper for the fitness functions.

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

    def __call__(self, solution, *moves):
        """Fill the fitness attribute of a solution.

        The fitness function will only be called if the fitness

        """
        if solution.fitness is None:
            solution.fitness = self._compute_fitness_value(solution, *moves)

    def _compute_fitness_value(self, solution, *moves):
        if moves and self.fitness_partial:
            return self.fitness_partial(solution, *moves)
        else:
            return self.fitness(solution)


class ObjectiveNoisy(object):
    """TODO"""
    def __init__(self, fitness, std, fitness_partial=None):
        super().__init__(fitness, fitness_partial)
        self.std = std

    def __call__(self, solution, *moves):
        super().__call__(solution, *moves)
