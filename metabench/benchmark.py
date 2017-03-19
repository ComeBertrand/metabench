"""
File: benchmark.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: A Benchmark is a performance study of one or several
metaheuristics on one or several problems.
"""

from itertools import product
from collections import OrderedDict


class Benchmark(object):
    """ Benchmark of metaheuristic(s) running on problem(s)."""
    def __init__(self):
        self._metaheuristics = []
        self._problems = []
        self._results = OrderedDict()

    def add_meta(self, metaheuristic_class, *args, **kwargs):
        """Add a metaheuristic to the Benchmark.

        Args:
            metaheuristic_class (Metaheuristic): The class of the metaheuristic
                to be evaluated.

        """
        self._metaheuristics.append((metaheuristic_class, args, kwargs))

    def add_problem(self, problem_class, *args, **kwargs):
        """Add a problem to the Benchmark.

        Args:
            problem_class (Problem): The problem on which the evaluation will
                take place.

        """
        self._problems.append((problem_class, args, kwargs))

    def run(self):
        """Compute the Benchmark."""

        self._results = OrderedDict()
        for meta, prob in product(self._metaheuristics, self._problems):
            meta_class, meta_attributes, meta_key_attributes = meta
            prob_class, prob_attributes, prob_key_attributes = prob
            problem = prob_class(*prob_attributes, **prob_key_attributes)
            metaheuristic = meta_class(problem,
                                       *meta_attributes,
                                       **meta_key_attributes)
            self._results[metaheuristic] = []

        for metaheuristic in self._results:
            for iter_stat in metaheuristic.run():
                self._results[metaheuristic].append(iter_stat)
