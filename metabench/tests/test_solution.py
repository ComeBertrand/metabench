import numpy as np

import metabench as mb
from metabench.tests.fixtures import *


def test_generation_solution_binary(binary_encoding):
    s = binary_encoding.generate_random_solution()
    assert isinstance(s, mb.Solution)
    assert s.encoding is binary_encoding
    assert s.fitness is None
    assert np.all(s <= 1)
    assert np.all(s >= 0)


def test_generation_solution_discrete(discrete_encoding):
    s = discrete_encoding.generate_random_solution()
    assert isinstance(s, mb.Solution)
    assert s.encoding is discrete_encoding
    assert s.fitness is None
    assert np.all(s <= MAX_VAL_INT)
    assert np.all(s >= MIN_VAL_INT)


def test_generation_solution_real(real_encoding):
    s = real_encoding.generate_random_solution()
    assert isinstance(s, mb.Solution)
    assert s.encoding is real_encoding
    assert s.fitness is None
    assert np.all(s <= MAX_VAL_FLO)
    assert np.all(s >= MIN_VAL_FLO)


def test_generation_solution_permutation(permutation_encoding):
    s = permutation_encoding.generate_random_solution()
    assert isinstance(s, mb.Solution)
    assert s.encoding is permutation_encoding
    assert s.fitness is None
    assert set(s) == set(permutation_encoding.items)


def test_copy_binary(binary_solution):
    binary_solution.fitness = 1.0
    c1 = binary_solution.copy(copy_fitness=False)
    assert c1 is not binary_solution
    assert c1.encoding is binary_solution.encoding
    assert c1.fitness is None
    c2 = binary_solution.copy(copy_fitness=True)
    assert c2 is not binary_solution
    assert c2.encoding is binary_solution.encoding
    assert c2.fitness == binary_solution.fitness


def test_copy_discrete(discrete_solution):
    discrete_solution.fitness = 1.0
    c1 = discrete_solution.copy(copy_fitness=False)
    assert c1 is not discrete_solution
    assert c1.encoding is discrete_solution.encoding
    assert c1.fitness is None
    c2 = discrete_solution.copy(copy_fitness=True)
    assert c2 is not discrete_solution
    assert c2.encoding is discrete_solution.encoding
    assert c2.fitness == discrete_solution.fitness


def test_copy_real(real_solution):
    real_solution.fitness = 1.0
    c1 = real_solution.copy(copy_fitness=False)
    assert c1 is not real_solution
    assert c1.encoding is real_solution.encoding
    assert c1.fitness is None
    c2 = real_solution.copy(copy_fitness=True)
    assert c2 is not real_solution
    assert c2.encoding is real_solution.encoding
    assert c2.fitness == real_solution.fitness


def test_copy_permutation(permutation_solution):
    permutation_solution.fitness = 1.0
    c1 = permutation_solution.copy(copy_fitness=False)
    assert c1 is not permutation_solution
    assert c1.encoding is permutation_solution.encoding
    assert c1.fitness is None
    c2 = permutation_solution.copy(copy_fitness=True)
    assert c2 is not permutation_solution
    assert c2.encoding is permutation_solution.encoding
    assert c2.fitness == permutation_solution.fitness


def test_max_min_val_binary(binary_solution):
    min_vals = binary_solution.min_vals()
    max_vals = binary_solution.max_vals()
    for i in range(NB_ATTRIBUTES):
        assert min_vals[i] == 0
        assert binary_solution.min_val(i) == 0
        assert max_vals[i] == 1
        assert binary_solution.max_val(i) == 1


def test_max_min_val_discrete(discrete_solution):
    min_vals = discrete_solution.min_vals()
    max_vals = discrete_solution.max_vals()
    for i in range(NB_ATTRIBUTES):
        assert min_vals[i] == MIN_VAL_INT
        assert discrete_solution.min_val(i) == MIN_VAL_INT
        assert max_vals[i] == MAX_VAL_INT
        assert discrete_solution.max_val(i) == MAX_VAL_INT


def test_max_min_val_real(real_solution):
    min_vals = real_solution.min_vals()
    max_vals = real_solution.max_vals()
    for i in range(NB_ATTRIBUTES):
        assert min_vals[i] == MIN_VAL_FLO
        assert real_solution.min_val(i) == MIN_VAL_FLO
        assert max_vals[i] == MAX_VAL_FLO
        assert real_solution.max_val(i) == MAX_VAL_FLO


def test_max_min_val_permutation(permutation_solution):
    min_vals = permutation_solution.min_vals()
    max_vals = permutation_solution.max_vals()
    assert min_vals is None
    assert max_vals is None
    for i in range(NB_ATTRIBUTES):
        assert permutation_solution.min_val(i) is None
        assert permutation_solution.max_val(i) is None


def test_to_bounds_binary_up(binary_solution):
    binary_solution += 2
    binary_solution.to_bounds()
    assert np.all(binary_solution == 1)


def test_to_bounds_binary_low(binary_solution):
    binary_solution -= 2
    binary_solution.to_bounds()
    assert np.all(binary_solution == 0)


def test_to_bounds_discrete_up(discrete_solution):
    discrete_solution += MAX_VAL_INT + 1
    discrete_solution.to_bounds()
    assert np.all(discrete_solution == MAX_VAL_INT)


def test_to_bounds_discrete_low(discrete_solution):
    discrete_solution -= (MAX_VAL_INT - MIN_VAL_INT) + 1
    discrete_solution.to_bounds()
    assert np.all(discrete_solution == MIN_VAL_INT)


def test_to_bounds_real_up(real_solution):
    real_solution += MAX_VAL_FLO + 1.0
    real_solution.to_bounds()
    assert np.all(real_solution == MAX_VAL_FLO)


def test_to_bounds_real_low(real_solution):
    real_solution -= (MAX_VAL_FLO - MIN_VAL_FLO) + 1.0
    real_solution.to_bounds()
    assert np.all(real_solution == MIN_VAL_FLO)
