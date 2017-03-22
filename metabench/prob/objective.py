"""
File: objective.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Wrappers for the fitness functions.
"""

from collections import OrderedDict


class Modifs(OrderedDict):
    """Keep track of the modifications made on a solution.

    The Modifs will be used to compute the fitness of a modified solution
    in a partial manner.

    Each key of a Modifs is the index of where the change was made, each
    value is a tuple of (value_before, value_after).

    """
    def __init__(self):
        super().__init__()

    def add_modif(self, index, val_before, val_after):
        """Add a modification to the list of moves.

        A new modif on an existing indexed move will see its new val_before
        dropped and its former val_after replaced. This insure that the modifs
        will always keep the first and last value of an attribute.

        Args:
            index (int): Index where the change was made in the solution.
            val_before (any): Previous value at the index.
            val_after (any): New value at the index.

        """
        cur_val = self.get(index, None)
        if cur_val is not None:
            super().__setitem__(index, (cur_val[0], val_after))
        else:
            super().__setitem__(index, (val_before, val_after))

    def __setitem__(self, key, value):
        """Only allow the setting of values through the add_modif method."""
        raise NotImplementedError("Use the add_modif method instead")


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
            modifs (Modifs): List of modifications made on the solution. Default
                is None.

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
        if solution.fitness and modifs and self.fitness_partial:
            return self.fitness_partial(solution, modifs)
        else:
            return self.fitness(solution)


class ObjectiveNoisy(object):
    """TODO"""
    def __init__(self, fitness, std, fitness_partial=None):
        super().__init__(fitness, fitness_partial)
        self.std = std

    def __call__(self, solution, modifs):
        super().__call__(solution, modifs)
