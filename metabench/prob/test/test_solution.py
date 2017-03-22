import pytest
import numpy as np

import metabench as mb


NB_ATTRIBUTES = 5
MIN_VAL_INT = 0
MAX_VAL_INT = 4
MIN_VAL_FLO = 0.0
MAX_VAL_FLO = 4.0


@pytest.fixture
def boundaries_int():
    min_bound_int = np.zeros(NB_ATTRIBUTES) + MIN_VAL_INT
    max_bound_int = np.zeros(NB_ATTRIBUTES) + MAX_VAL_INT
    return mb.Boundaries(min_bound_int, max_bound_int, type=np.int)


@pytest.fixture
def boundaries_float():
    min_bound_float = np.zeros(NB_ATTRIBUTES, np.float) + MIN_VAL_FLO
    max_bound_float = np.zeros(NB_ATTRIBUTES, np.float) + MAX_VAL_FLO
    return mb.Boundaries(min_bound_float, max_bound_float, type=np.float)


@pytest.fixture
def items():
    return np.array(range(NB_ATTRIBUTES), np.int)


@pytest.fixture
def binary_encoding():
    return mb.BinaryEncoding(NB_ATTRIBUTES)


@pytest.fixture
def binary_solution(binary_encoding):
    return binary_encoding.generate_random_solution()


@pytest.fixture
def discrete_encoding(boundaries_int):
    return mb.DiscreteEncoding(boundaries_int)


@pytest.fixture
def discrete_solution(discrete_encoding):
    return discrete_encoding.generate_random_solution()


@pytest.fixture
def real_encoding(boundaries_float):
    return mb.RealEncoding(boundaries_float)


@pytest.fixture
def real_solution(real_encoding):
    return real_encoding.generate_random_solution()


@pytest.fixture
def permutation_encoding(items):
    return mb.PermutationEncoding(items)


@pytest.fixture
def permutation_solution(permutation_encoding):
    return permutation_encoding.generate_random_solution()


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
    for i in range(NB_ATTRIBUTES):
        assert binary_solution.min_val(i) == 0
        assert binary_solution.max_val(i) == 1


def test_max_min_val_discrete(discrete_solution):
    for i in range(NB_ATTRIBUTES):
        assert discrete_solution.min_val(i) == MIN_VAL_INT
        assert discrete_solution.max_val(i) == MAX_VAL_INT


def test_max_min_val_real(real_solution):
    for i in range(NB_ATTRIBUTES):
        assert real_solution.min_val(i) == MIN_VAL_FLO
        assert real_solution.max_val(i) == MAX_VAL_FLO


def test_max_min_val_permutation(permutation_solution):
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
