"""
File: hill_climbing.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""

from metabench.meta.metaheuristic import SMetaheuristic


class HillClimbing(SMetaheuristic):
    def _get_initial_solution(self):
        return self.problem.generate_solution()

    def _get_candidates(self, solution):
        candidates = [n for n in self.problem.get_neighbors(solution)]
        return candidates

    def _select_solution(self, solution, candidates):
        self.problem.evaluate(solution)
        for c in candidates:
            self.problem.evaluate(c)
