"""
MetaBench
=========

    MetaBench (MB) is a Python package for the automated creation of benchmarks
    to evaluate the performance of metaheuristics on several types of problems.

Using
-----

    Just write in Python

    >>> import metabench as mb
    >>> b = mb.Benchmark(10)
    >>> b.add_meta(mb.default.HillClimbing)
    >>> b.add_prob(mb.default.Sphere, 10)
    >>> b.run()
    >>> print(b)
    --------------------------------------------------------------
    |                         METABENCH                          |
    --------------------------------------------------------------
    --------------------------------------------------------------
    |                      Problem : Sphere                      |
    |                     Meta : HillClimbing                    |
    |                        Nb runs : 10                        |
    --------------------------------------------------------------
    --------------------------------------------------------------
    |                          fitness                           |
    --------------------------------------------------------------
    |    worst     |     mean     |     best     |      std      |
    --------------------------------------------------------------
    |17.7823522216 |1.80963201638 |     0.0      | 5.32506287339 |
    --------------------------------------------------------------
    |                       nb_iterations                        |
    --------------------------------------------------------------
    |    worst     |     mean     |     best     |      std      |
    --------------------------------------------------------------
    |      8       |     5.7      |      5       |      0.9      |
    --------------------------------------------------------------
    |                     time_per_iteration                     |
    --------------------------------------------------------------
    |    worst     |     mean     |     best     |      std      |
    --------------------------------------------------------------
    |   0.13283    |0.0634562280702|   0.060117   |0.0101106443511|
    --------------------------------------------------------------
    |                        time_per_run                        |
    --------------------------------------------------------------
    |    worst     |     mean     |     best     |      std      |
    --------------------------------------------------------------
    |   0.491008   |  0.3626799   |   0.307602   |0.0657834396934|
    --------------------------------------------------------------

"""

import sys
if sys.version_info[0] < 3:
    message = "Python 3 is required for Metabench ({:d}.{:d} detected)."
    raise ImportError(message.format(sys.version_info[:2]))
del sys


__author__ = 'Come Bertrand'
__license__ = 'MIT License'
__version__ = '0.0.1'


from .common import *
from . import default
from .display import *
from .models import *
from .operators import *
from .utils import *
