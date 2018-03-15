MetaBench
=========

MetaBench (MB) is a Python package for the automated creation of benchmarks
to evaluate the performance of metaheuristics on several types of problems.


[![Build Status](https://travis-ci.org/ComeBertrand/metabench.svg?branch=master)](https://travis-ci.org/ComeBertrand/metabench)
[![Coverage Status](https://coveralls.io/repos/github/ComeBertrand/metabench/badge.svg?branch=master)](https://coveralls.io/github/ComeBertrand/metabench?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8fb2b18cc20346cb9ad4bff00e945ad8)](https://www.codacy.com/app/ComeBertrand/metabench?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ComeBertrand/metabench&amp;utm_campaign=Badge_Grade)



Using
-----

Just write in Python

```python
>>> from metabench.algorithmics.benchmark import Benchmark
>>> from metabench.algorithmics.problem.continuous import Sphere
>>> from metabench.algorithmics.metaheuristics.hill_climbing import HillClimbing
>>> b = Benchmark(10)
>>> b.add_meta(HillClimbing)
>>> b.add_prob(Sphere, 10)
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
```
