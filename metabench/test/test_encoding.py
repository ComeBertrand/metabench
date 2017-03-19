import math

import pytest
import numpy as np

import metabench.prob.encoding as enc


NB_ATTRIBUTES = 5
MIN_VAL_INT = 0
MAX_VAL_INT = 4
MIN_VAL_FLO = 0.0
MAX_VAL_FLO = 4.0


@pytest.fixture
def min_bound_int():
    return np.zeros(NB_ATTRIBUTES) + MIN_VAL_INT


@pytest.fixture
def max_bound_int():
    return np.zeros(NB_ATTRIBUTES) + MAX_VAL_INT


@pytest.fixture
def boundaries_int(min_bound_int, max_bound_int):
    return enc.Boundaries(min_bound_int, max_bound_int, type=np.int)


@pytest.fixture
def min_bound_float():
    return np.zeros(NB_ATTRIBUTES, np.float) + MIN_VAL_FLO


@pytest.fixture
def max_bound_float():
    return np.zeros(NB_ATTRIBUTES, np.float) + MAX_VAL_FLO


@pytest.fixture
def boundaries_float(min_bound_float, max_bound_float):
    return enc.Boundaries(min_bound_float, max_bound_float, type=np.float)


@pytest.fixture
def list_items():
    return np.array(range(NB_ATTRIBUTES), np.int)


def test_boundaries_creation_int(min_bound_int, max_bound_int):
    b = enc.Boundaries(min_bound_int, max_bound_int, type=np.int)
    assert len(b) == 3
    assert len(b[0]) == NB_ATTRIBUTES
    assert len(b[1]) == NB_ATTRIBUTES
    assert len(b[2]) == NB_ATTRIBUTES
    assert np.all(b[0] == MIN_VAL_INT)
    assert np.all(b[1] == MAX_VAL_INT)
    assert np.all(b[2] == MAX_VAL_INT - MIN_VAL_INT)


def test_boundaries_creation_float(min_bound_float, max_bound_float):
    b = enc.Boundaries(min_bound_float, max_bound_float, type=np.float)
    assert len(b) == 3
    assert len(b[0]) == NB_ATTRIBUTES
    assert len(b[1]) == NB_ATTRIBUTES
    assert len(b[2]) == NB_ATTRIBUTES
    assert np.all(b[0] == MIN_VAL_FLO)
    assert np.all(b[1] == MAX_VAL_FLO)
    assert np.all(np.isclose(b[2], (MAX_VAL_FLO - MIN_VAL_FLO)))


def test_boundaries_length_min_max(min_bound_int):
    max_bound = np.zeros(len(min_bound_int)+2, np.int) + MAX_VAL_INT
    with pytest.raises(ValueError):
        enc.Boundaries(min_bound_int, max_bound)


def test_boundaries_min_over_max(min_bound_int, max_bound_int):
    with pytest.raises(ValueError):
        enc.Boundaries(max_bound_int, min_bound_int, type=np.int)


def test_boundaries_epsilon(min_bound_float):
    b = enc.Boundaries(min_bound_float, min_bound_float, type=np.float)
    assert b[2][0] > 0.0


def test_binary_encoding_creation():
    e = enc.BinaryEncoding(NB_ATTRIBUTES)
    assert e.size == NB_ATTRIBUTES
    assert np.all(e.boundaries[0] == 0)
    assert np.all(e.boundaries[1] == 1)
    assert np.all(e.boundaries[2] == 1)


def test_binary_encoding_creation_negative_size():
    with pytest.raises(ValueError):
        enc.BinaryEncoding(-1)


def test_binary_encoding_space_size():
    c = enc.BinaryEncoding(NB_ATTRIBUTES)
    assert c.space_size() == 2 ** NB_ATTRIBUTES


def test_binary_encoding_generate():
    e = enc.BinaryEncoding(NB_ATTRIBUTES)
    s = e.generate_random_solution()
    assert np.all(s <= 1)
    assert np.all(s >= 0)


def test_discrete_encoding_creation_wrong_boundaries(boundaries_float):
    with pytest.raises(TypeError):
        enc.DiscreteEncoding(boundaries_float)


def test_discrete_encoding_generate(boundaries_int):
    e = enc.DiscreteEncoding(boundaries_int)
    s = e.generate_random_solution()
    assert np.all(s <= MAX_VAL_INT)
    assert np.all(s >= MIN_VAL_INT)


def test_discrete_encoding_space_size(boundaries_int):
    e = enc.DiscreteEncoding(boundaries_int)
    assert e.space_size() == (1 + MAX_VAL_INT - MIN_VAL_INT) ** NB_ATTRIBUTES


def test_real_encoding_creation_wrong_boundaries(boundaries_int):
    with pytest.raises(TypeError):
        enc.RealEncoding(boundaries_int)


def test_real_encoding_generate(boundaries_float):
    e = enc.RealEncoding(boundaries_float)
    s = e.generate_random_solution()
    assert np.all(s <= MAX_VAL_FLO)
    assert np.all(s >= MIN_VAL_FLO)


def test_permutation_encoding_generate(list_items):
    e = enc.PermutationEncoding(list_items)
    s = e.generate_random_solution()
    assert set(s) == set(list_items)


def test_permutation_encoding_space_size(list_items):
    e = enc.PermutationEncoding(list_items)
    assert e.space_size() == math.factorial(len(list_items))
