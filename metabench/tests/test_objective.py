import pytest

import metabench as mb
from metabench.tests.fixtures import *


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
                              binary_solution,
                              modifs_as_modifs,
                              modifs_empty):
    o = mb.Objective(fitness_func)

    binary_solution.fitness = None
    assert o._compute_fitness_value(binary_solution, None) == VALUE_RETURNED_FIT
    o(binary_solution)
    assert binary_solution.fitness == VALUE_RETURNED_FIT

    binary_solution.fitness = None
    assert (o._compute_fitness_value(binary_solution, modifs_as_modifs) ==
            VALUE_RETURNED_FIT)
    o(binary_solution, modifs_as_modifs)
    assert binary_solution.fitness == VALUE_RETURNED_FIT

    binary_solution.fitness = None
    assert (o._compute_fitness_value(binary_solution, modifs_empty) ==
            VALUE_RETURNED_FIT)
    o(binary_solution, modifs_empty)
    assert binary_solution.fitness == VALUE_RETURNED_FIT


def test_objective_no_partial_fitness(fitness_func,
                                      binary_solution,
                                      modifs_as_modifs,
                                      modifs_empty):
    o = mb.Objective(fitness_func)

    binary_solution.fitness = VALUE_NOT_RETURNED
    assert o._compute_fitness_value(binary_solution, None) == VALUE_RETURNED_FIT
    o(binary_solution)
    assert binary_solution.fitness == VALUE_NOT_RETURNED

    binary_solution.fitness = VALUE_NOT_RETURNED
    assert (o._compute_fitness_value(binary_solution, modifs_as_modifs) ==
            VALUE_RETURNED_FIT)
    o(binary_solution, modifs_as_modifs)
    assert binary_solution.fitness == VALUE_RETURNED_FIT

    binary_solution.fitness = VALUE_NOT_RETURNED
    assert (o._compute_fitness_value(binary_solution, modifs_empty) ==
            VALUE_RETURNED_FIT)
    o(binary_solution, modifs_empty)
    assert binary_solution.fitness == VALUE_RETURNED_FIT


def test_objective_partial(fitness_func,
                           fitness_partial_func,
                           binary_solution,
                           modifs_as_modifs,
                           modifs_empty):
    o = mb.Objective(fitness_func, fitness_partial_func)

    binary_solution.fitness = None
    assert o._compute_fitness_value(binary_solution, None) == VALUE_RETURNED_FIT
    o(binary_solution)
    assert binary_solution.fitness == VALUE_RETURNED_FIT

    binary_solution.fitness = None
    assert (o._compute_fitness_value(binary_solution, modifs_as_modifs) ==
            VALUE_RETURNED_FIT)
    o(binary_solution, modifs_as_modifs)
    assert binary_solution.fitness == VALUE_RETURNED_FIT

    binary_solution.fitness = None
    assert (o._compute_fitness_value(binary_solution, modifs_empty) ==
            VALUE_RETURNED_FIT)
    o(binary_solution, modifs_empty)
    assert binary_solution.fitness == VALUE_RETURNED_FIT


def test_objective_partial_fitness(fitness_func,
                                   fitness_partial_func,
                                   binary_solution,
                                   modifs_as_modifs,
                                   modifs_empty):
    o = mb.Objective(fitness_func, fitness_partial_func)

    binary_solution.fitness = VALUE_NOT_RETURNED
    assert o._compute_fitness_value(binary_solution, None) == VALUE_RETURNED_FIT
    o(binary_solution)
    assert binary_solution.fitness == VALUE_NOT_RETURNED

    binary_solution.fitness = VALUE_NOT_RETURNED
    assert (o._compute_fitness_value(binary_solution, modifs_as_modifs) ==
            VALUE_RETURNED_FIT_PART)
    o(binary_solution, modifs)
    assert binary_solution.fitness == VALUE_RETURNED_FIT_PART

    binary_solution.fitness = VALUE_NOT_RETURNED
    assert (o._compute_fitness_value(binary_solution, modifs_empty) ==
            VALUE_RETURNED_FIT)
    o(binary_solution, modifs_empty)
    assert binary_solution.fitness == VALUE_RETURNED_FIT
