"""
File: benchmark.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: A Benchmark is a performance study of one or several
metaheuristics on one or several problems.
"""

from time import clock
from collections import defaultdict
from itertools import product

from ..display import draw_benchmark_statistics
from .statistics import StatisticsRecorder


class Benchmark(object):
    """ Benchmark of metaheuristic(s) running on problem(s)."""
    def __init__(self, nb_runs):
        self._nb_runs = nb_runs
        self._metaheuristics = []
        self._problems = []
        self._results = defaultdict(lambda: defaultdict())

    def add_meta(self, metaheuristic_class, *args, **kwargs):
        """Add a metaheuristic to the Benchmark.

        Args:
            metaheuristic_class (Metaheuristic): The class of the metaheuristic
                to be evaluated.

        """
        self._metaheuristics.append((metaheuristic_class, args, kwargs))

    def add_prob(self, problem_class, *args, **kwargs):
        """Add a problem to the Benchmark.

        Args:
            problem_class (Problem): The problem on which the evaluation will
                take place.

        """
        self._problems.append((problem_class, args, kwargs))

    def run(self):
        """Compute the Benchmark."""
        # TODO: add tqdm for time of computation
        self._results = defaultdict(lambda: defaultdict())

        for i, j in product(range(len(self._problems)), range(len(self._metaheuristics))):
            self._results[i][j] = StatisticsRecorder(self._nb_runs, self._problems[i][0], self._metaheuristics[j][0])
            self._compute(i, j)

    def _compute(self, index_prob, index_meta):
        stats = self._results[index_prob][index_meta]

        prob = self._problems[index_prob]
        meta = self._metaheuristics[index_meta]

        prob_class, prob_attributes, prob_key_attributes = prob
        problem = prob_class(*prob_attributes, **prob_key_attributes)

        meta_class, meta_attributes, meta_key_attributes = meta

        for i in range(self._nb_runs):
            print("> Meta [{}] - Prob [{}] - Run num "
                  "{:d}".format(meta_class.__name__,
                                prob_class.__name__,
                                i))
            metaheuristic = meta_class(problem,
                                       *meta_attributes,
                                       **meta_key_attributes)
            t_run = t_iter = clock()
            for solution in metaheuristic.run():
                diff_t_iter = clock() - t_iter
                stats.record_iter_stat(i, solution, diff_t_iter)
                t_iter = clock()

            diff_t_run = clock() - t_run
            stats.record_time_computation(i, diff_t_run)

    def display(self):
        draw_benchmark_statistics(self._results)

    def __str__(self):
        line = "".join(["-"]*62) + "\n"
        b_str = ""
        b_str += line
        b_str += "|{}|\n".format("METABENCH".center(60))
        b_str += line
        for index_prob in self._results:
            for index_meta in self._results[index_prob]:
                stats = self._results[index_prob][index_meta]
                prob = self._problems[index_prob]
                meta = self._metaheuristics[index_meta]
                prob_class, prob_attributes, prob_key_attributes = prob
                meta_class, meta_attributes, meta_key_attributes = meta
                b_str += line
                b_str += "|{}|\n".format(" Problem : {}".format(
                    prob_class.__name__).center(60))
                b_str += "|{}|\n".format(" Meta : {}".format(
                    meta_class.__name__).center(60))
                b_str += "|{}|\n".format(" Nb runs : {:d}".format(
                    self._nb_runs).center(60))
                b_str += line
                b_str += str(stats)
        return b_str
