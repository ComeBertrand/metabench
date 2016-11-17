class Metaheuristic(object):
    """ Abstract class for metaheuristics.

    An instance of a metaheuristic is associated to a specific problem
    to be solved.

    Attributes:
        problem (Problem) : the problem that the metaheuristic will
            solve.

    """

    def __init__(self, problem, **kwargs):
        self.problem = problem

    def __iter__(self):
        """ Iteration of the metaheuristic on the given problem.

        Returns:
            iter_stat (IterStat) : statistic of the behaviour and result
                of the metaheuristic at the end of this iteration.
        """
        raise NotImplementedError("Abstract Class")
