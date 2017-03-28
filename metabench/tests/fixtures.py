import pytest
import numpy as np

import metabench as mb


NB_ATTRIBUTES = 5
MIN_VAL_INT = 0
MAX_VAL_INT = 4
MIN_VAL_FLO = 0.0
MAX_VAL_FLO = 4.0

VALUE_NOT_RETURNED = 0
VALUE_RETURNED_FIT = 1
VALUE_RETURNED_FIT_PART = 2

NB_NEIGHBORS = 10
STEP = 0.04

NB_RUNS = 3
NB_RUNS_FALSE = -3
NB_ITER = 10
BASE_SIZE = 256
BASE_SIZE_FALSE = -256


@pytest.fixture
def min_bound_int():
    return np.zeros(NB_ATTRIBUTES) + MIN_VAL_INT


@pytest.fixture
def max_bound_int():
    return np.zeros(NB_ATTRIBUTES) + MAX_VAL_INT


@pytest.fixture
def boundaries_int(min_bound_int, max_bound_int):
    return mb.Boundaries(min_bound_int, max_bound_int, type=np.int)


@pytest.fixture
def min_bound_float():
    return np.zeros(NB_ATTRIBUTES, np.float) + MIN_VAL_FLO


@pytest.fixture
def max_bound_float():
    return np.zeros(NB_ATTRIBUTES, np.float) + MAX_VAL_FLO


@pytest.fixture
def boundaries_float(min_bound_float, max_bound_float):
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


@pytest.fixture
def fitness_func():
    def fitness(solution):
        return VALUE_RETURNED_FIT
    return fitness


@pytest.fixture
def fitness_partial_func():
    def fitness_partial(solution, modifs):
        return VALUE_RETURNED_FIT_PART
    return fitness_partial


@pytest.fixture
def modifs():
    return [(0, 'a', 'b'), (1, 'c', 'd'), (2, 'e', 'f')]


@pytest.fixture
def modifs_double():
    return [(0, 'a', 'b'), (0, 'b', 'c')], (0, 'a', 'c')


@pytest.fixture
def modifs_as_modifs(modifs):
    m = mb.Modifs()
    for index, val_bef, val_aft in modifs:
        m.add_modif(index, val_bef, val_aft)
    return m


@pytest.fixture
def modifs_empty():
    return mb.Modifs()


@pytest.fixture
def one_type_name_permutation():
    return 'PermutationEncoding'


@pytest.fixture
def two_type_names_binary_discrete():
    return ['BinaryEncoding', 'DiscreteEncoding']


@pytest.fixture
def empty_statistics():
    return mb.Statistics(NB_RUNS, BASE_SIZE)


@pytest.fixture
def list_records(binary_encoding):
    full_list_records = []
    for i in range(NB_RUNS):
        list_solutions = [binary_encoding.generate_random_solution() for
                          j in range(NB_ITER)]
        for f, s in enumerate(list_solutions[::-1]):
            s.fitness = f + i
        full_list_records += [(i, s, t) for t, s in enumerate(list_solutions)]
    return full_list_records


@pytest.fixture
def list_time_tot():
    return [i for i in range(NB_RUNS)]


@pytest.fixture
def param_creation_some():
    return {'attr_int': 25,
            'attr_enum': 'A'}


@pytest.fixture
def param_creation_all():
    return {'attr_int': 25,
            'attr_float': 2.0,
            'attr_str': 'Test String',
            'attr_enum': 'A'}
