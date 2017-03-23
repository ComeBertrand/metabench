import numpy as np

import metabench as mb
from metabench.tests.fixtures import *


def test_binary_flip(binary_solution):
    neighborhood = [(n, m) for n, m in mb.move_binary_flip(binary_solution)]
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


def test_move_continuous(real_solution):
    neighborhood = [(n, m) for n, m in
                    mb.move_distance_continuous(real_solution, STEP,
                                                NB_NEIGHBORS)]
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


def test_substitution(discrete_solution):
    neighborhood = [(n, m) for n, m in mb.move_substitution(discrete_solution)]
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


def test_swap(permutation_solution):
    neighborhood = [(n, m) for n, m in mb.move_swap(permutation_solution)]
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
