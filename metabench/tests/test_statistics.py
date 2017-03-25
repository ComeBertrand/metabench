import pytest
import numpy as np

import metabench as mb
from metabench.tests.fixtures import *


def test_statistics_creation():
    mb.Statistics(NB_RUNS, BASE_SIZE)
    with pytest.raises(ValueError):
        mb.Statistics(NB_RUNS_FALSE, BASE_SIZE)
    with pytest.raises(ValueError):
        mb.Statistics(NB_RUNS, BASE_SIZE_FALSE)


def test_empty_statistics(empty_statistics):
    assert empty_statistics.nb_run == NB_RUNS
    assert np.all(empty_statistics.nb_iter_per_run == np.zeros(NB_RUNS,
                                                               np.int))
    assert empty_statistics.nb_iter_total == 0
    assert len(empty_statistics.best_values) == 0
    assert empty_statistics.best_value is None
    assert empty_statistics.worst_value is None
    assert empty_statistics.mean_value is None
    assert empty_statistics.std_value is None
    assert empty_statistics.best_time_iter is None
    assert empty_statistics.worst_time_iter is None
    assert empty_statistics.mean_time_iter is None
    assert empty_statistics.std_time_iter is None
    assert empty_statistics.best_time_tot is None
    assert empty_statistics.worst_time_tot is None
    assert empty_statistics.mean_time_tot is None
    assert empty_statistics.std_time_tot is None


def test_rec_stat_iter_unevaluated_sol(empty_statistics, binary_solution):
    with pytest.raises(ValueError):
        empty_statistics.record_iter_stat(0, binary_solution, 0.0)


def test_rec_stat_iter(empty_statistics, list_records):
    for num_run, sol, time in list_records:
        empty_statistics.record_iter_stat(num_run, sol, time)

    assert empty_statistics.nb_run == NB_RUNS
    assert np.all(empty_statistics.nb_iter_per_run == (np.zeros(NB_RUNS,
                                                               np.int)
                                                       +
                                                       NB_ITER))
    assert empty_statistics.nb_iter_total == NB_RUNS * NB_ITER
    assert len(empty_statistics.best_values) == NB_RUNS
    assert np.all(empty_statistics.best_values == np.array([i for i in range(NB_RUNS)], np.float))
    assert empty_statistics.best_time_iter == 0
    assert empty_statistics.worst_time_iter == (NB_ITER) - 1
    assert empty_statistics.best_time_tot is None
    assert empty_statistics.worst_time_tot is None
    assert empty_statistics.mean_time_tot is None
    assert empty_statistics.std_time_tot is None


def test_rec_stat_time_tot(empty_statistics, list_time_tot):
    for i, t in enumerate(list_time_tot):
        empty_statistics.record_time_computation(i, t)

    assert empty_statistics.best_time_tot == float(0)
    assert empty_statistics.worst_time_tot == float(NB_RUNS - 1)
