import pytest

import metabench as mb
from metabench.tests.fixtures import *


def test_not_implemented_one_type(fitness_func,
                                  binary_solution,
                                  discrete_solution,
                                  real_solution,
                                  permutation_solution,
                                  one_type_name_permutation):
    decorator = mb.not_implemented_for(one_type_name_permutation)
    f = decorator(fitness_func)
    f(binary_solution)
    f(discrete_solution)
    f(real_solution)
    with pytest.raises(NotImplementedError):
        f(permutation_solution)


def test_not_implemented_two_type(fitness_func,
                                  binary_solution,
                                  discrete_solution,
                                  real_solution,
                                  permutation_solution,
                                  two_type_names_binary_discrete):
    decorator = mb.not_implemented_for(*two_type_names_binary_discrete)
    f = decorator(fitness_func)
    with pytest.raises(NotImplementedError):
        f(binary_solution)
    with pytest.raises(NotImplementedError):
        f(discrete_solution)
    f(real_solution)
    f(permutation_solution)


def test_implemented_one_type(fitness_func,
                              binary_solution,
                              discrete_solution,
                              real_solution,
                              permutation_solution,
                              one_type_name_permutation):
    decorator = mb.implemented_for(one_type_name_permutation)
    f = decorator(fitness_func)
    with pytest.raises(NotImplementedError):
        f(binary_solution)
    with pytest.raises(NotImplementedError):
        f(discrete_solution)
    with pytest.raises(NotImplementedError):
        f(real_solution)
    f(permutation_solution)


def test_implemented_two_type(fitness_func,
                              binary_solution,
                              discrete_solution,
                              real_solution,
                              permutation_solution,
                              two_type_names_binary_discrete):
    decorator = mb.implemented_for(*two_type_names_binary_discrete)
    f = decorator(fitness_func)
    f(binary_solution)
    f(discrete_solution)
    with pytest.raises(NotImplementedError):
        f(real_solution)
    with pytest.raises(NotImplementedError):
        f(permutation_solution)
