import pytest

import metabench as mb


NB_ATTRIBUTES = 5
VALUE_NOT_RETURNED = 0
VALUE_RETURNED_FIT = 1
VALUE_RETURNED_FIT_PART = 2


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
def solution():
    e = mb.BinaryEncoding(NB_ATTRIBUTES)
    return e.generate_random_solution()


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


def test_modifs_add_modif(modifs):
    m = mb.Modifs()
    for index, val_bef, val_aft in modifs:
        m.add_modif(index, val_bef, val_aft)

    for i in range(len(modifs)):
        assert m.get(modifs[i][0], None) == modifs[i][1:]


def test_modifs_add_double_modif(modifs_double):
    modifs, expected = modifs_double
    m = mb.Modifs()
    for index, val_bef, val_aft in modifs:
        m.add_modif(index, val_bef, val_aft)

    assert m.get(expected[0], None) == expected[1:]


def test_modifs_setitem(modifs):
    m = mb.Modifs()
    with pytest.raises(NotImplementedError):
        m[0] = ('a', 'b')


def test_objective_no_partial(fitness_func,
                              solution,
                              modifs_as_modifs,
                              modifs_empty):
    o = Objective(fitness_func)

    solution.fitness = None
    assert o._compute_fitness_value(solution, None) == VALUE_RETURNED_FIT
    o(solution)
    assert solution.fitness == VALUE_RETURNED_FIT

    solution.fitness = None
    assert o._compute_fitness_value(solution, modifs_as_modifs) == VALUE_RETURNED_FIT
    o(solution, modifs_as_modifs)
    assert solution.fitness == VALUE_RETURNED_FIT

    solution.fitness = None
    assert o._compute_fitness_value(solution, modifs_empty) == VALUE_RETURNED_FIT
    o(solution, modifs_empty)
    assert solution.fitness == VALUE_RETURNED_FIT


def test_objective_no_partial_fitness(fitness_func,
                                      solution,
                                      modifs_as_modifs,
                                      modifs_empty):
    o = Objective(fitness_func)

    solution.fitness = VALUE_NOT_RETURNED
    assert o._compute_fitness_value(solution, None) == VALUE_RETURNED_FIT
    o(solution)
    assert solution.fitness == VALUE_NOT_RETURNED

    solution.fitness = VALUE_NOT_RETURNED
    assert o._compute_fitness_value(solution, modifs_as_modifs) == VALUE_RETURNED_FIT
    o(solution, modifs_as_modifs)
    assert solution.fitness == VALUE_RETURNED_FIT

    solution.fitness = VALUE_NOT_RETURNED
    assert o._compute_fitness_value(solution, modifs_empty) == VALUE_RETURNED_FIT
    o(solution, modifs_empty)
    assert solution.fitness == VALUE_RETURNED_FIT


def test_objective_partial(fitness_func,
                           fitness_partial_func,
                           solution,
                           modifs_as_modifs,
                           modifs_empty):
    o = Objective(fitness_func, fitness_partial_func)

    solution.fitness = None
    assert o._compute_fitness_value(solution, None) == VALUE_RETURNED_FIT
    o(solution)
    assert solution.fitness == VALUE_RETURNED_FIT

    solution.fitness = None
    assert o._compute_fitness_value(solution, modifs_as_modifs) == VALUE_RETURNED_FIT
    o(solution, modifs_as_modifs)
    assert solution.fitness == VALUE_RETURNED_FIT

    solution.fitness = None
    assert o._compute_fitness_value(solution, modifs_empty) == VALUE_RETURNED_FIT
    o(solution, modifs_empty)
    assert solution.fitness == VALUE_RETURNED_FIT


def test_objective_partial_fitness(fitness_func,
                                   fitness_partial_func,
                                   solution,
                                   modifs_as_modifs,
                                   modifs_empty):
    o = Objective(fitness_func, fitness_partial_func)

    solution.fitness = VALUE_NOT_RETURNED
    assert o._compute_fitness_value(solution, None) == VALUE_RETURNED_FIT
    o(solution)
    assert solution.fitness == VALUE_NOT_RETURNED

    solution.fitness = VALUE_NOT_RETURNED
    assert o._compute_fitness_value(solution, modifs_as_modifs) == VALUE_RETURNED_FIT_PART
    o(solution, modifs)
    assert solution.fitness == VALUE_RETURNED_FIT_PART

    solution.fitness = VALUE_NOT_RETURNED
    assert o._compute_fitness_value(solution, modifs_empty) == VALUE_RETURNED_FIT
    o(solution, modifs_empty)
    assert solution.fitness == VALUE_RETURNED_FIT
