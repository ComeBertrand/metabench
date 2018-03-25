"""
File: hill_climbing.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Naive implementation of the Hill Climbing algorithm.
"""

from ...models import SMetaheuristic


class HillClimbing(SMetaheuristic):
    """Hill Climbing metaheuristic.

    Args:
        base_step (float): Base step used for the descent. Must be between
            0.0 and 1.0. Default is 0.1 (which represent a slow descent).

    Attributes:
        previous_fitness (float): Best fitness of the previous iteration.
        base_step (float): Base step used for the descent.

    """
    def __init__(self, problem, base_step=0.1):
        super().__init__(problem)
        self.previous_fitness = None
        self.base_step = base_step

    def _get_initial_solution(self):
        solution = self.problem.generate_solution()
        self.problem.evaluate(solution)
        return solution

    def _get_candidates(self):
        candidates = [(c, m) for c, m in
                      self.problem.get_neighbors(self.solution,
                                                 self.base_step)]
        return candidates

    def _select_solution(self, candidates):
        best_fitness = self.solution.fitness
        best_candidate = self.solution
        for c, m in candidates:
            self.problem.evaluate(c, m)
            if c.fitness <= best_fitness:
                best_fitness = c.fitness
                best_candidate = c

        return best_candidate

    def _stopping_criterion(self):
        unchanged = ((self.previous_fitness is not None) and
                     (self.previous_fitness <= self.solution.fitness))
        if unchanged:
            return True

        self.previous_fitness = self.solution.fitness
        return False
