"""
MetaBench
=========

    MetaBench (MB) is a Python package for the automated creation of benchmarks
    to evaluate the performance of metaheuristics on several types of problems.

Using
-----

    Just write in Python

    >>> import metabench as mb
    >>> B = mb.Benchmark()
    >>> B.add_meta(mb.meta.HillClimbing)
    >>> B.add_problem(mb.prob.Sphere, 10, 0, 100)
    >>> B.run()
    >>> for meta, list_stats in B._results.items():
    ...     for stat in list_stats:
    ...         print(stat.best)
    6624.562194808384
    870.9916120787564
    7.033312961340519
    0.0
    0.0

"""

import sys
if sys.version_info[0] < 3:
    m = "Python 3 is required for Metabench ({:d}.{:d} detected)."
    raise ImportError(m.format(sys.version_info[:2]))
del sys


__author__ = 'Come Bertrand'
__license__ = 'MIT License'
__version__ = '0.0.1'


from metabench.benchmark import *
from metabench.draw import *
from metabench.statistics import *

from metabench.prob.solution import *
from metabench.prob.problem import *
from metabench.prob.objective import *
from metabench.prob.encoding import *
from metabench.prob.constraint import *
from metabench.prob.operators.neighborhood import *

from metabench.misc.decorators import *

from metabench.meta.metaheuristic import *
