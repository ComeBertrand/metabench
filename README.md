MetaBench
=========

MetaBench (MB) is a Python package for the automated creation of benchmarks
to evaluate the performance of metaheuristics on several types of problems.


[![Build Status](https://travis-ci.org/ComeBertrand/metabench.svg?branch=master)](https://travis-ci.org/ComeBertrand/metabench)
[![Coverage Status](https://coveralls.io/repos/github/ComeBertrand/metabench/badge.svg?branch=master)](https://coveralls.io/github/ComeBertrand/metabench?branch=master)



Using
-----

Just write in Python

```python
>>> import metabench as mb
>>> b = mb.Benchmark()
>>> b.add_meta(mb.meta.HillClimbing)
>>> b.add_prob(mb.prob.Sphere, 10, 0, 100)
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
