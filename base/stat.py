class IterStat(object):
    """ Compilation of statistics on a metaheuristic iteration.
    """
    def __init__(self, iter_num, best=None, lowest=None, avg=None,
                 std=None, time=None):
        self.iter_num = iter_num
        self.best = best
        self.lowest = lowest
        self.avg = avg
        self.std = std
        self.time = time
