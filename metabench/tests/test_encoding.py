import math

import numpy as np

from metabench.common.representation import *
from metabench.common.representation.encoding import Encoding
from metabench.tests.fixtures import *


def test_boundaries_creation_int(min_bound_int, max_bound_int):
    b = Boundaries(min_bound_int, max_bound_int, type=np.int)
    assert len(b) == 3
    assert len(b[0]) == NB_ATTRIBUTES
    assert len(b[1]) == NB_ATTRIBUTES
    assert len(b[2]) == NB_ATTRIBUTES
    assert np.all(b[0] == MIN_VAL_INT)
    assert np.all(b[1] == MAX_VAL_INT)
    assert np.all(b[2] == MAX_VAL_INT - MIN_VAL_INT)


def test_boundaries_creation_float(min_bound_float, max_bound_float):
    b = Boundaries(min_bound_float, max_bound_float, type=np.float)
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
        Boundaries(min_bound_int, max_bound)


def test_boundaries_min_over_max(min_bound_int, max_bound_int):
    with pytest.raises(ValueError):
        Boundaries(max_bound_int, min_bound_int, type=np.int)


def test_boundaries_epsilon(min_bound_float):
    b = Boundaries(min_bound_float, min_bound_float, type=np.float)
    assert b[2][0] > 0.0


def test_boundaries_int_min_max_val(min_bound_int, max_bound_int):
    b = Boundaries(min_bound_int, max_bound_int, type=np.int)
    min_vals = b.min_vals()
    max_vals = b.max_vals()
    for i in range(NB_ATTRIBUTES):
        assert min_vals[i] == min_bound_int[i]
        assert b.min_val(i) == min_bound_int[i]
        assert max_vals[i] == max_bound_int[i]
        assert b.max_val(i) == max_bound_int[i]


def test_boundaries_float_min_max_val(min_bound_float, max_bound_float):
    b = Boundaries(min_bound_float, max_bound_float, type=np.float)
    min_vals = b.min_vals()
    max_vals = b.max_vals()
    for i in range(NB_ATTRIBUTES):
        assert min_vals[i] == min_bound_float[i]
        assert b.min_val(i) == min_bound_float[i]
        assert max_vals[i] == max_bound_float[i]
        assert b.max_val(i) == max_bound_float[i]


def test_binary_encoding_creation():
    e = BinaryEncoding(NB_ATTRIBUTES)
    assert e.size == NB_ATTRIBUTES
    assert np.all(e.boundaries[0] == 0)
    assert np.all(e.boundaries[1] == 1)
    assert np.all(e.boundaries[2] == 1)


def test_binary_encoding_creation_negative_size():
    with pytest.raises(ValueError):
        BinaryEncoding(-1)


def test_binary_encoding_space_size():
    c = BinaryEncoding(NB_ATTRIBUTES)
    assert c.space_size() == 2 ** NB_ATTRIBUTES


def test_binary_encoding_generate():
    e = BinaryEncoding(NB_ATTRIBUTES)
    s = e.generate_random_value()
    assert np.all(s <= 1)
    assert np.all(s >= 0)


def test_discrete_encoding_creation_wrong_boundaries(boundaries_float):
    with pytest.raises(TypeError):
        DiscreteEncoding(boundaries_float)


def test_discrete_encoding_generate(boundaries_int):
    e = DiscreteEncoding(boundaries_int)
    s = e.generate_random_value()
    assert np.all(s <= MAX_VAL_INT)
    assert np.all(s >= MIN_VAL_INT)


def test_discrete_encoding_space_size(boundaries_int):
    e = DiscreteEncoding(boundaries_int)
    assert e.space_size() == (1 + MAX_VAL_INT - MIN_VAL_INT) ** NB_ATTRIBUTES


def test_real_encoding_creation_wrong_boundaries(boundaries_int):
    with pytest.raises(TypeError):
        RealEncoding(boundaries_int)


def test_real_encoding_generate(boundaries_float):
    e = RealEncoding(boundaries_float)
    s = e.generate_random_value()
    assert np.all(s <= MAX_VAL_FLO)
    assert np.all(s >= MIN_VAL_FLO)


def test_real_encoding_space_size(boundaries_float):
    e = RealEncoding(boundaries_float)
    with pytest.raises(NotImplementedError):
        e.space_size()


def test_permutation_encoding_generate(items):
    e = PermutationEncoding(items)
    s = e.generate_random_value()
    assert set(s) == set(items)


def test_permutation_encoding_space_size(items):
    e = PermutationEncoding(items)
    assert e.space_size() == math.factorial(len(items))


def test_encoding_abstract_generate():
    e = Encoding()
    with pytest.raises(NotImplementedError):
        e.generate_random_value()


def test_encoding_abstract_space():
    e = Encoding()
    with pytest.raises(NotImplementedError):
        e.space_size()


def test_encoding_abstract_distance_no_ord():
    e = Encoding()
    with pytest.raises(NotImplementedError):
        e.distance(1, 2)
