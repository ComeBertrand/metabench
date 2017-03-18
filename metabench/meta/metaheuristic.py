"""
File: metaheuristic.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""


class Metaheuristic(object):

    """Docstring for Metaheuristic.

    Args:
        problem

    Attributes:
        problem

    """

    def __init__(self, problem):
        self.problem = problem

    def run(self):
        """
        """
        raise NotImplementedError('Abstract Class')


class SMetaheuristic(Metaheuristic):
    def __init__(self, problem, *args, **kwargs):
        super().__init__(problem)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        solution = self._get_initial_solution()
        candidates = None
        while not self._stopping_criterion(solution, candidates):
            candidates = self._get_candidates(solution)
            solution = self._select_solution(solution, candidates)

        return solution

    def _get_initial_solution(self):
        raise NotImplementedError('Abstract Class')

    def _get_candidates(self, solution):
        raise NotImplementedError('Abstract Class')

    def _select_solution(self, solution, candidates):
        raise NotImplementedError('Abstract Class')

    def _stopping_criterion(self, solution, candidates):
        raise NotImplementedError('Abstract Class')
