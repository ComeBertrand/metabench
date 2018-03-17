"""
File: abstract.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Base classes for the Metaheuristics.
"""


class Metaheuristic(object):
    """Optimization computer that will work on a Problem.

    Args:
        problem (Problem): the problem to be optimized.

    Attributes:
        problem (Problem): the problem to be optimized.
        solution (Solution): the current best solution found.

    """

    def __init__(self, problem):
        self.problem = problem
        self.solution = None

    def run(self):
        """Compute to find the best solution of the problem.

        Yield:
            Solution: Best solution for the current iteration.

        """
        raise NotImplementedError('Abstract Class')


class SMetaheuristic(Metaheuristic):
    """Solution based metaheuristic.

    Solution based metaheuristics iterate to improve a single solution by
    trying to improve it by replacing it by its one its neighbors.

    """

    def run(self):
        self.solution = self._get_initial_solution()
        while not self._stopping_criterion():
            candidates = self._get_candidates()
            self.solution = self._select_solution(candidates)
            yield self.solution

    def _get_initial_solution(self):
        """Fetch the starting solution.

        Returns:
            Solution: the starting solution.

        """
        raise NotImplementedError('Abstract Class')

    def _get_candidates(self):
        """Get the candidate solutions for the current iteration.

        The next solution will be taken from those candidates.

        Returns:
            list: of Solution, the neighboring candidates.

        """
        raise NotImplementedError('Abstract Class')

    def _select_solution(self, candidates):
        """Select the next iteration solution from the candidates solution.

        Args:
            candidates (list): of Solution, the candidates solution to replace
                the current one.

        Returns:
            Solution: The best candidates for the iteration.

        """
        raise NotImplementedError('Abstract Class')

    def _stopping_criterion(self):
        """Stopping criterion of the iterative process.

        Returns:
            bool: True if the computation should end, False otherwise.

        """
        raise NotImplementedError('Abstract Class')
