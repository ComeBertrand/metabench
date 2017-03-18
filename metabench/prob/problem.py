"""
File: problem.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""


class Problem(object):
    def __init__(self, objective, encoding, neighborhood=None):
        self.objective = objective
        self.encoding = encoding
        self.neighborhood = neighborhood

    def evaluate(self, solution, *moves):
        self.objective(solution, *moves)

    def generate_solution(self):
        return self.encoding.generate_random_solution()

    def get_neighbors(self, solution):
        if self.neighborhood is not None:
            for neighbor in self.neighborhood(solution):
                yield neighbor
        else:
            raise NotImplementedError('No neighborhood operator is implemented'
                                      ' for this problem.')
