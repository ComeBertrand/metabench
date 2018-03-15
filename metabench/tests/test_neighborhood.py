import numpy as np

from metabench.tests.fixtures import *
from metabench.algorithmic.operators.neighborhood import *


def test_binary_one_flip(binary_solution):
    neighborhood = [(n, m) for n, m in move_binary_flip(binary_solution, 1, None)]
    assert len(neighborhood) == NB_ATTRIBUTES
    for index, vals in enumerate(neighborhood):
        n, m = neighborhood[index]
        assert n is not binary_solution
        assert n.encoding is binary_solution.encoding
        assert len(n) == NB_ATTRIBUTES
        assert len(m) == 1
        for i in range(NB_ATTRIBUTES):
            if i in m:
                assert binary_solution[i] == m[i][0]
                assert n[i] == m[i][1]
                if binary_solution[i]:
                    assert n[i] == 0
                else:
                    assert n[i] == 1
            else:
                assert n[i] == binary_solution[i]


def test_binary_two_flip(binary_solution):
    neighborhood = [(n, m) for n, m in move_binary_flip(binary_solution, 2, 10)]
    assert len(neighborhood) == 10
    for index, vals in enumerate(neighborhood):
        n, m = neighborhood[index]
        assert n is not binary_solution
        assert n.encoding is binary_solution.encoding
        assert len(n) == NB_ATTRIBUTES
        assert len(m) == 2
        for i in range(NB_ATTRIBUTES):
            if i in m:
                assert binary_solution[i] == m[i][0]
                assert n[i] == m[i][1]
                if binary_solution[i]:
                    assert n[i] == 0
                else:
                    assert n[i] == 1
            else:
                assert n[i] == binary_solution[i]


def test_move_continuous(real_solution):
    neighborhood = [(n, m) for n, m in move_distance_continuous(real_solution, STEP, NB_NEIGHBORS)]
    assert len(neighborhood) == NB_NEIGHBORS
    for index, vals in enumerate(neighborhood):
        n, m = neighborhood[index]
        assert n is not real_solution
        assert n.encoding is real_solution.encoding
        assert len(n) == NB_ATTRIBUTES
        assert len(m) == 0
        assert np.linalg.norm(real_solution - n) <= STEP + (STEP / 10000.0)
        assert np.all(n <= real_solution.max_vals())
        assert np.all(n >= real_solution.min_vals())


def test_one_substitution(discrete_solution):
    neighborhood = [(n, m) for n, m in move_substitution(discrete_solution, 1, None)]
    assert len(neighborhood) == (NB_ATTRIBUTES * (MAX_VAL_INT - MIN_VAL_INT))
    for index, vals in enumerate(neighborhood):
        n, m = neighborhood[index]
        assert n is not discrete_solution
        assert n.encoding is discrete_solution.encoding
        assert len(n) == NB_ATTRIBUTES
        assert len(m) == 1
        assert np.linalg.norm(discrete_solution - n, ord=0) == 1
        for i in range(NB_ATTRIBUTES):
            if i in m:
                assert discrete_solution[i] == m[i][0]
                assert n[i] == m[i][1]
                assert discrete_solution[i] != n[i]
            else:
                assert n[i] == discrete_solution[i]


def test_two_substitution(discrete_solution):
    neighborhood = [(n, m) for n, m in move_substitution(discrete_solution, 2, 10)]
    assert len(neighborhood) == 10
    for index, vals in enumerate(neighborhood):
        n, m = neighborhood[index]
        assert n is not discrete_solution
        assert n.encoding is discrete_solution.encoding
        assert len(n) == NB_ATTRIBUTES
        assert len(m) == 2
        assert np.linalg.norm(discrete_solution - n, ord=0) == 2
        for i in range(NB_ATTRIBUTES):
            if i in m:
                assert discrete_solution[i] == m[i][0]
                assert n[i] == m[i][1]
                assert discrete_solution[i] != n[i]
            else:
                assert n[i] == discrete_solution[i]


def test_one_swap(permutation_solution):
    neighborhood = [(n, m) for n, m in move_swap(permutation_solution, 1, None)]
    assert len(neighborhood) == (NB_ATTRIBUTES * (NB_ATTRIBUTES - 1)) / 2
    for index, vals in enumerate(neighborhood):
        n, m = neighborhood[index]
        assert n is not permutation_solution
        assert n.encoding is permutation_solution.encoding
        assert len(n) == NB_ATTRIBUTES
        assert len(m) == 2
        assert np.linalg.norm(permutation_solution - n, ord=0) == 2
        for i in range(NB_ATTRIBUTES):
            if i in m:
                assert permutation_solution[i] == m[i][0]
                assert n[i] == m[i][1]
                assert permutation_solution[i] != n[i]
            else:
                assert n[i] == permutation_solution[i]

        i, j = m.keys()
        assert permutation_solution[i] == n[j]
        assert permutation_solution[j] == n[i]


def test_two_swap(permutation_solution):
    neighborhood = [(n, m) for n, m in move_swap(permutation_solution, 2, 10)]
    assert len(neighborhood) == 10
    for index, vals in enumerate(neighborhood):
        n, m = neighborhood[index]
        assert n is not permutation_solution
        assert n.encoding is permutation_solution.encoding
        assert len(n) == NB_ATTRIBUTES
        assert len(m) == 4
        assert np.linalg.norm(permutation_solution - n, ord=0) == 4
        for i in range(NB_ATTRIBUTES):
            if i in m:
                assert permutation_solution[i] == m[i][0]
                assert n[i] == m[i][1]
                assert permutation_solution[i] != n[i]
            else:
                assert n[i] == permutation_solution[i]

        i, j, k, l = m.keys()
        assert permutation_solution[i] == n[j]
        assert permutation_solution[j] == n[i]
        assert permutation_solution[k] == n[l]
        assert permutation_solution[l] == n[k]


def test_move_range_check_step(continuous_move_range):
    continuous_move_range._check_step(0.3)
    continuous_move_range._check_step(0.)
    continuous_move_range._check_step(1.)
    with pytest.raises(TypeError):
        continuous_move_range._check_step(3)
    with pytest.raises(ValueError):
        continuous_move_range._check_step(-0.1)
    with pytest.raises(ValueError):
        continuous_move_range._check_step(1.1)


def test_continuous_mv_creation():
    cmv = ContinuousMoveRange(MIN_VAL_FLO, MAX_VAL_FLO)
    with pytest.raises(ValueError):
        ContinuousMoveRange(MIN_VAL_FLO + 1.0, MIN_VAL_FLO)
    with pytest.raises(TypeError):
        ContinuousMoveRange(MIN_VAL_INT, MAX_VAL_FLO)
    with pytest.raises(TypeError):
        ContinuousMoveRange(MIN_VAL_FLO, MAX_VAL_INT)


def test_discrete_mv_creation():
    dmv = DiscreteMoveRange(MIN_VAL_INT, MAX_VAL_INT)
    with pytest.raises(ValueError):
        DiscreteMoveRange(MIN_VAL_INT + 1, MIN_VAL_INT)
    with pytest.raises(TypeError):
        DiscreteMoveRange(MIN_VAL_INT, MAX_VAL_FLO)
    with pytest.raises(TypeError):
        DiscreteMoveRange(MIN_VAL_FLO, MAX_VAL_INT)


def test_cmv_convert(continuous_move_range):
    for i in range(101):
        step = i / 100.
        assert MIN_VAL_FLO <= continuous_move_range.convert(step) <= MAX_VAL_FLO


def test_cmv_log_convert(continuous_log_move_range):
    for i in range(101):
        step = i / 100.
        assert MIN_VAL_FLO_LMV <= continuous_log_move_range.convert(step) <= MAX_VAL_FLO_LMV


def test_dmv_convert(discrete_move_range):
    vals = set([x for x in range(MIN_VAL_INT, MAX_VAL_INT + 1)])
    for i in range(101):
        step = i / 100.
        assert discrete_move_range.convert(step) in vals


def test_dmv_log_convert(discrete_log_move_range):
    vals = set([x for x in range(MIN_VAL_INT, MAX_VAL_INT + 1)])
    for i in range(101):
        step = i / 100.
        assert discrete_log_move_range.convert(step) in vals


def test_neighborhood(real_solution, continuous_move_range):
    n = NeighborhoodGenerator(move_distance_continuous, continuous_move_range, NB_NEIGHBORS)
    list_neighbors = [neighbor for neighbor, _ in n(real_solution, 0.5)]

    max_dist = continuous_move_range.convert(0.5)
    assert len(list_neighbors) == NB_NEIGHBORS
    for neighbor in list_neighbors:
        dist = np.linalg.norm(real_solution - neighbor)
        assert dist <= max_dist + 0.00001
