from itertools import product
from collections import OrderedDict


class Benchmark(object):
    """ Benchmark of metaheuristic(s) runs on problem(s).

    """
    def __init__(self):
        self.metaheuristics = []
        self.problems = []
        self.results = OrderedDict()

    def add_metaheuristic(self, metaheuristic_class, *args, **kwargs):
        self.metaheuristics.append((metaheuristic_class, args, kwargs))

    def add_problem(self, problem_class, *args, **kwargs):
        self.problems.append((problem_class, args, kwargs))

    def run(self):
        self.results = OrderedDict()
        for meta, prob in product(self.metaheuristics, self.problems):
            meta_class, meta_attributes, meta_key_attributes = meta
            prob_class, prob_attributes, prob_key_attributes = prob
            problem = prob_class(*prob_attributes, **prob_key_attributes)
            metaheuristic = meta_class(problem,
                                       *meta_attributes,
                                       **meta_key_attributes)
            self.results[metaheuristic] = []

        for metaheuristic in self.results:
            for iter_stat in metaheuristic:
                self.results[metaheuristic].append(iter_stat)
