MetaBench
=========

    MetaBench (MB) is a Python package for the automated creation of benchmarks
    to evaluate the performance of metaheuristics on several types of problems.


[![Build
Status](https://travis-ci.org/ComeBertrand/metabench.svg?branch=master)](https://travis-ci.org/ComeBertrand/metabench)


Using
-----

    Just write in Python

    ```python
    >>> import metabench as mb
    >>> B = mb.Benchmark()
    >>> B.add_meta(mb.meta.HillClimbing)
    >>> B.add_problem(mb.prob.Sphere, 10, 0, 100)
    >>> B.run()
    >>> for meta, list_stats in B._results.items():
    ...     for stat in list_stats:
    ...         print(stat.best)
    13975.488179892573
    4360.568874224535
    2547.5959016063475
    2547.5959016063475
    ```
