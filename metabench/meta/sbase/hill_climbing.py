"""
File: hill_climbing.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Naive implementation of the Hill Climbing algorithm.
"""

from metabench.meta.metaheuristic import SMetaheuristic


class HillClimbing(SMetaheuristic):
    """Hill Climbing metaheuristic.

    Attributes:
        previous_fitness (float): Best fitness of the previous iteration.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_fitness = None

    def _get_initial_solution(self):
        solution = self.problem.generate_solution()
        self.problem.evaluate(solution)
        return solution

    def _get_candidates(self):
        candidates = [(n, m) for n, m in self.problem.get_neighbors(self.solution)]
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
